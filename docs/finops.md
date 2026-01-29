# FinOps Automation and Cost Optimization

This document explains the FinOps strategy implemented in this project to control cloud costs automatically.

---

## Problem

In cloud environments, idle EC2 instances often remain running and continue generating costs even when not actively used.

This project implements an automated workflow to:
- Detect idle EC2 instances
- Record idle history
- Notify administrators
- Safely stop unused instances

---

## FinOps Architecture Overview

Services used:
- Amazon CloudWatch
- AWS Lambda
- Amazon DynamoDB
- Amazon EventBridge
- Amazon SNS

---

## Step 1: Idle EC2 Detection

**Lambda Function:** `detect-idle-ec2`

Logic:
- Fetch running EC2 instances
- Read CPUUtilization from CloudWatch
- If CPU < 5% for extended duration:
  - Tag instance:
    - `IdleCandidate=true`
    - `IdleDetectedAt=<timestamp>`

Purpose:
- Identify cost-wasting resources
- Create foundation for automation

---

## Step 2: Idle History Logging

**DynamoDB Table:** `IdleInstances`

Attributes stored:
- InstanceId
- DetectedAt (epoch timestamp)
- DetectedAtISO
- CPUAverage

This enables:
- Historical tracking
- Audit trail
- Safe decision making

---

## Step 3: Scheduled Evaluation

**EventBridge Rule**
- Runs on a schedule (daily in production)
- Triggers idle detection automatically

Used higher frequency temporarily during testing only.

---

## Step 4: Safe Auto-Stop Workflow

**Lambda Function:** `idle-actioner`

Features:
- Reads idle EC2 records from DynamoDB
- Applies safety checks:
  - Owner tag verification
  - DoNotStop tag exclusion
- Sends SNS email notification before action

**Action Modes:**
- `dryrun` → notify only
- `stop` → stop EC2 instance safely

Default mode is `dryrun` to prevent accidental shutdown.

---

## Notifications

**Amazon SNS**
- Sends email alerts before stop action
- Provides transparency and control

---

## Cost Safety Measures

- Default ACTION_MODE = dryrun
- Manual review before enabling stop mode
- EC2 stop preserves EBS data
- No termination performed automatically

---

## Outcome

- Automated idle detection implemented
- Zero accidental instance termination
- Reduced unnecessary EC2 runtime
- Full visibility of cost-saving actions

This FinOps approach reflects real-world cloud cost governance practices.
