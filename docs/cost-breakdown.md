# AWS Cost Breakdown

This document summarizes the cost behavior of the project during development and testing.

---

## AWS Account Type

- AWS Free Tier account
- Promotional credits available
- Region: ap-south-1 (Mumbai)

---

## Services Used

| Service | Purpose |
|------|------|
| EC2 | Application servers |
| Auto Scaling | Self-healing & scaling |
| Application Load Balancer | Traffic distribution |
| Lambda | Automation & FinOps |
| DynamoDB | Idle tracking |
| CloudWatch | Monitoring & alarms |
| SNS | Email notifications |
| EventBridge | Scheduled automation |

---

## Cost Monitoring Tools

- AWS Cost Explorer
- AWS Free Tier Usage Dashboard
- Cost Anomaly Detection
- AWS Budgets ($1–$2 threshold)

---

## Observed Cost Pattern

- Majority usage remained within Free Tier
- EC2 usage minimized via:
  - Instance stopping after testing
  - No long-running workloads
- Lambda and DynamoDB usage remained negligible

---

## Cost Optimization Practices

- EC2 instances not kept running continuously
- Auto Scaling min capacity adjusted after tests
- EventBridge scheduled daily (not frequent)
- Alarms and alerts enabled

---

## Final Observations

- Total cost remained extremely low
- No unexpected billing spikes
- Anomaly detection configured for safety
- Project demonstrates cost-aware cloud engineering

---

## Conclusion

This project was designed to demonstrate:
- Technical architecture
- Operational reliability
- Cost governance awareness

All services were used responsibly following FinOps best practices.
