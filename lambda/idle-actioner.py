import os
import boto3
import time
import datetime
import traceback

dynamodb = boto3.resource("dynamodb")
ec2 = boto3.client("ec2")
sns = boto3.client("sns")

TABLE_NAME = os.environ.get("TABLE_NAME", "IdleInstances")
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")
ACTION_MODE = os.environ.get("ACTION_MODE", "dryrun").lower()  # dryrun or stop
IDLE_THRESHOLD_MINUTES = int(os.environ.get("IDLE_THRESHOLD_MINUTES", "60"))

table = dynamodb.Table(TABLE_NAME)

def now_epoch():
    return int(time.time())

def iso_now():
    return datetime.datetime.utcnow().isoformat()

def find_idle_items_older_than(threshold_minutes):
    """
    We stored items with DetectedAt epoch number.
    Scan the table for items where DetectedAt <= now - threshold_seconds and
    (Optionally) check that we haven't already acted on it.
    """
    cutoff = now_epoch() - (threshold_minutes * 60)
    response = table.scan(
        FilterExpression = boto3.dynamodb.conditions.Attr('DetectedAt').lte(cutoff)
    )
    items = response.get('Items', [])
    return items

def mark_item_actioned(instance_id, detected_at, action, note=None):
    # Update item with Action, ActionAt timestamp
    key = {'InstanceId': instance_id, 'DetectedAt': int(detected_at)}
    update_expr = "SET #a = :a, ActionAt = :ts"
    expr_attr_names = {'#a':'Action'}
    expr_attr_vals = {':a': action, ':ts': now_epoch()}
    if note:
        update_expr += ", Note = :n"
        expr_attr_vals[':n'] = note
    table.update_item(
        Key=key,
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_attr_names,
        ExpressionAttributeValues=expr_attr_vals
    )

def publish_sns(subject, message):
    if not SNS_TOPIC_ARN:
        print("SNS_TOPIC_ARN not set; skipping publish")
        return
    resp = sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject,
        Message=message
    )
    print("SNS publish response:", resp.get('MessageId'))

def stop_instance(instance_id):
    print("Stopping instance:", instance_id)
    resp = ec2.stop_instances(InstanceIds=[instance_id])
    print("Stop response:", resp)
    return resp

def lambda_handler(event, context):
    print("idle-actioner started. ACTION_MODE =", ACTION_MODE, "threshold mins =", IDLE_THRESHOLD_MINUTES)
    try:
        items = find_idle_items_older_than(IDLE_THRESHOLD_MINUTES)
        print("Found items older than threshold:", len(items))
        if not items:
            return {"actioned": []}

        actioned = []
        for item in items:
            instance_id = item.get('InstanceId')
            detected_at = item.get('DetectedAt')
            cpu = item.get('CPUAvg', 'unknown')
            try:
                # Safety checks: do not stop instances with protection tags or different owner
                # Query EC2 for tags
                inst = ec2.describe_instances(InstanceIds=[instance_id])
                tags = {}
                for r in inst.get('Reservations', []):
                    for i in r.get('Instances', []):
                        for t in i.get('Tags', []):
                            tags[t['Key']] = t['Value']

                # Skip if Owner not Satvik (safety)
                if tags.get('Owner') and tags.get('Owner') != 'Satvik':
                    print("Skipping", instance_id, "Owner != Satvik")
                    mark_item_actioned(instance_id, detected_at, "skipped-owner", "Owner not Satvik")
                    continue

                # Skip if custom protection tag present
                if tags.get('DoNotStop') == 'true':
                    print("Skipping", instance_id, "DoNotStop tag present")
                    mark_item_actioned(instance_id, detected_at, "skipped-protection", "DoNotStop tag")
                    continue

                # Notify before action
                subject = f"[FinOps] Idle action for {instance_id}"
                message = (
                    f"Instance {instance_id} was detected idle at {item.get('DetectedAtISO','unknown')} "
                    f"with CPUAvg={cpu}. ACTION_MODE={ACTION_MODE}.\n\n"
                    f"This message is from idle-actioner Lambda at {iso_now()}."
                )
                publish_sns(subject, message)

                if ACTION_MODE == "stop":
                    # Stop instance
                    stop_instance(instance_id)
                    mark_item_actioned(instance_id, detected_at, "stopped", "Stopped by idle-actioner")
                    actioned.append({"InstanceId": instance_id, "Action": "stopped"})
                else:
                    # dryrun
                    mark_item_actioned(instance_id, detected_at, "not-stopped-dryrun", "Dryrun only")
                    actioned.append({"InstanceId": instance_id, "Action": "dryrun"})
            except Exception as e:
                print("Error while processing", instance_id, e)
                print(traceback.format_exc())
                mark_item_actioned(instance_id, detected_at, "error", str(e))
        return {"actioned": actioned}
    except Exception as e:
        print("Fatal error", e)
        print(traceback.format_exc())
        return {"error": str(e)}
