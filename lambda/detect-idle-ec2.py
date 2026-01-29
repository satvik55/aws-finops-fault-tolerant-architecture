import boto3
import datetime
import time
import traceback

dynamo = boto3.resource("dynamodb")
cloudwatch = boto3.client("cloudwatch")
ec2 = boto3.client("ec2")
TABLE_NAME = "IdleInstances"

def put_idle_record(table, instance_id, cpu_avg, detected_at_iso):
    # detected_at_epoch as number for sort key
    ts = int(time.time())
    item = {
        "InstanceId": instance_id,
        "DetectedAt": ts,
        "DetectedAtISO": detected_at_iso,
        "CPUAvg": str(cpu_avg) if cpu_avg is not None else "null"
    }
    table.put_item(Item=item)

def lambda_handler(event, context):
    print("Lambda started - detect-idle-ec2")
    table = dynamo.Table(TABLE_NAME)

    try:
        # Get running instances
        resp = ec2.describe_instances(Filters=[
            {"Name": "instance-state-name", "Values": ["running"]}
        ])

        running_instances = []
        for r in resp.get("Reservations", []):
            for i in r.get("Instances", []):
                running_instances.append(i["InstanceId"])

        print("Found instances:", running_instances)

        if not running_instances:
            print("No instances running right now.")
            return {"idle": []}

        idle_instances = []
        end = datetime.datetime.utcnow()
        start = end - datetime.timedelta(minutes=60)
        detected_at_iso = end.isoformat()

        for instance_id in running_instances:
            try:
                metric = cloudwatch.get_metric_statistics(
                    Namespace="AWS/EC2",
                    MetricName="CPUUtilization",
                    Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
                    StartTime=start,
                    EndTime=end,
                    Period=300,
                    Statistics=['Average']
                )

                dps = metric.get("Datapoints", [])
                print(f"{instance_id} metric datapoints:", dps)

                cpu_avg = None
                if dps:
                    cpu_avg = sorted(dps, key=lambda x: x["Timestamp"])[-1]["Average"]

                print(f"{instance_id} CPU Avg:", cpu_avg)

                if cpu_avg is not None and cpu_avg < 5:
                    idle_instances.append(instance_id)

                    # Tag the EC2 instance as idle (you already do this)
                    try:
                        ec2.create_tags(
                            Resources=[instance_id],
                            Tags=[
                                {"Key": "IdleCandidate", "Value": "true"},
                                {"Key": "IdleDetectedAt", "Value": detected_at_iso}
                            ]
                        )
                        print(f"Tagged {instance_id} as IdleCandidate")
                    except Exception as tag_err:
                        print(f"Failed to tag {instance_id}:", tag_err)
                        print(traceback.format_exc())

                    # Put item into DynamoDB
                    try:
                        put_idle_record(table, instance_id, cpu_avg, detected_at_iso)
                        print(f"Logged {instance_id} to DynamoDB")
                    except Exception as ddb_err:
                        print("DynamoDB put failed:", ddb_err)
                        print(traceback.format_exc())

            except Exception as inst_err:
                print("Error fetching metric for", instance_id, inst_err)
                print(traceback.format_exc())

        print("Idle Instances:", idle_instances)
        return {"idle": idle_instances}

    except Exception as e:
        print("ERROR:", e)
        print(traceback.format_exc())
        return {"error": str(e)}
