# 🚀 AWS FinOps & Fault-Tolerant Automation System

---

## 📌 Project Overview

This project demonstrates a **production-style AWS architecture** focused on:

- High Availability  
- Fault Tolerance  
- Cost Optimization (FinOps)  
- Automated monitoring and self-healing  

The system simulates how real organizations design cloud infrastructure that is **resilient, observable, and cost-controlled**.

**Region:** ap-south-1 (Mumbai)

---

## 🧩 Architecture Summary

- Multi-AZ deployment using Auto Scaling Group  
- Application Load Balancer for traffic distribution  
- Automated self-healing on instance failure  
- FinOps automation using Lambda + DynamoDB  
- Full observability via CloudWatch dashboards  
- Cost governance via budgets and anomaly detection  

📐 **Architecture diagram available in:**  
`architecture/final-architecture.png`

---

## ⚙️ Key Features

### ✅ Fault Tolerance
- Auto Scaling Group replaces unhealthy EC2 instances automatically  
- Tested single-instance and multi-instance failures  
- Recovery without manual intervention  

### ✅ High Availability
- Instances distributed across multiple Availability Zones  
- ALB ensures continuous traffic routing  

### ✅ FinOps Automation
- Detects idle EC2 instances automatically  
- Logs idle resources into DynamoDB  
- Safe auto-stop workflow with dry-run mode  
- SNS notifications before any action  

### ✅ Observability
- Central CloudWatch dashboard  
- EC2, ASG, ALB, Lambda, alarms in one view  
- Real-time operational visibility  

### ✅ Cost Governance
- AWS Budgets with alerts  
- Cost Anomaly Detection enabled  
- Free Tier monitoring  
- No unexpected billing  

---

## ☁️ AWS Services Used

- Amazon EC2  
- Auto Scaling Group  
- Application Load Balancer (ALB)  
- CloudWatch (metrics, alarms, dashboards)  
- AWS Lambda  
- Amazon DynamoDB  
- Amazon EventBridge  
- Amazon SNS  
- AWS Budgets  
- Cost Explorer  
- Cost Anomaly Detection  

---

## 🔄 FinOps Automation Flow

### detect-idle-ec2 Lambda
- Reads EC2 CPU metrics  
- Tags idle instances  
- Logs idle history to DynamoDB  

### EventBridge Scheduler
- Triggers detection automatically  

### idle-actioner Lambda
- Evaluates idle duration  
- Performs safety checks  
- Sends SNS notification  
- Supports dry-run and stop modes  

### DynamoDB
- Maintains audit trail of idle actions  

---

## 🛡️ Fault Tolerance & Reliability

### RTO / RPO Testing

- **Single instance failure:** Recovery time ≈ 1–2 minutes  
- **Multiple instance failure:** Auto Scaling recreated instances automatically  
- **RPO:** Stateless application → no data loss (RPO ≈ 0)  

📄 Detailed report available in:  
`docs/rto-rpo.md`

---

## 📊 Monitoring & Observability

CloudWatch dashboard includes:

- EC2 CPU utilization  
- ASG desired & in-service instances  
- ALB request count  
- Target group health  
- Lambda invocations  
- Alarm states  
- Cost metrics  

**Dashboard name:** `finops-ft-dashboard`

---

## 💰 Cost Governance

- Monthly budget with alert threshold  
- Free Tier monitoring enabled  
- Cost Anomaly Detection active  
- ALB cost kept minimal  
- EC2 stopped after testing  

Documentation available in:
- `docs/finops.md`  
- `docs/cost-breakdown.md`  

---

## 📁 Project Folder Structure

aws-finops-fault-tolerant-architecture/
|
|-- architecture/
| |-- final-architecture.png
|
|-- screenshots/
| |-- day11-dashboard.png
| |-- day12-failure-recovery.png
| |-- day14-auto-scaling.png
| |-- day15-operations-dashboard.png
|
|-- lambda/
| |-- detect-idle-ec2.py
| |-- idle-actioner.py
|
|-- docs/
| |-- rto-rpo.md
| |-- finops.md
| |-- cost-breakdown.md
|
|-- README.md


---

## 🧠 Learning Outcomes

- Designed real-world AWS architecture  
- Implemented self-healing systems  
- Understood FinOps principles deeply  
- Practiced cost-aware cloud engineering  
- Built production-style monitoring  
- Learned how to document systems professionally  

---

## 👤 Author

**Satvik Bodke**  
AWS Cloud & FinOps Enthusiast
