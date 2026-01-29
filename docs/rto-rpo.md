# RTO / RPO Testing Report

This document summarizes fault tolerance testing performed on the AWS Auto Scaling architecture.

---

## Test 1: Single EC2 Instance Failure

**Scenario:**  
One EC2 instance in the Auto Scaling Group was terminated manually to simulate a server-level failure.

**Observed Behavior:**
- Auto Scaling detected unhealthy instance via EC2 health checks
- Instance was terminated automatically
- New EC2 instance was launched using launch template
- Target Group health returned to healthy
- Application traffic continued via ALB

**Results:**
- Recovery Time Objective (RTO): ~1 minute 49 seconds
- Recovery was fully automated
- No manual intervention required

---

## Test 2: Multiple Instance Failure (Simulated AZ-like Event)

**Scenario:**  
Both EC2 instances were terminated to simulate a severe availability event.

**Observed Behavior:**
- Auto Scaling detected unhealthy state
- New instances launched automatically
- ALB resumed routing once targets became healthy

**Results:**
- Recovery Time Objective (RTO): ~1 minute 53 seconds
- Application fully recovered automatically

---

## Recovery Point Objective (RPO)

- Application is stateless (Apache static web content)
- No persistent data stored on EC2
- No database dependency

**RPO:** ≈ 0 (no data loss)

---

## Post-Test Cost Control

After testing:
- Auto Scaling desired capacity reduced
- No EC2 instances kept running
- AMI and Launch Template retained (no hourly compute cost)

---

## Summary

| Metric | Result |
|------|------|
| Self-healing | ✅ Yes |
| Multi-instance recovery | ✅ Yes |
| Manual intervention | ❌ Not required |
| RTO | ~2 minutes |
| RPO | ~0 |
