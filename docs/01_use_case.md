# Use Case: What the agent should actually do

Input:
> payment-api is returning 5xx errors.

The desired workflow is:

```text
Understand incident
  ↓
Discover exact resources
  ↓
Gather live evidence
  ↓
List concrete issues
  ↓
Find likely RCA
  ↓
Create resource-specific remediation
  ↓
Human approval if mutation is required
  ↓
Execute allowlisted action
  ↓
Verify
  ↓
Resolved? ---- no ----> Investigate again
  |
 yes
  ↓
Report
```

## Good vs bad output

Bad:
> Check logs and restart the pod.

Good:
> Issue: payments/payment-api-7d9c8f7b6f-x2k9m is in CrashLoopBackOff.
>
> Evidence: restart count 14; last termination reason OOMKilled; memory limit 256Mi.
>
> Impact: this replica is unavailable and deployment capacity is reduced.
>
> Remediation: target deployment/payment-api in namespace payments; inspect memory usage and configured limits, then apply the smallest tested change. Approval required.
>
> Verification: rollout readiness, restart count, health endpoint and error rate.

The exact names and values must come from live tools; the example values are illustrative.

## Why the loop matters

The agent should not always run the same commands.

If `kubectl get pods` shows Running, it should not blindly restart the pod. It may instead inspect logs, events, service endpoints or dependencies.

The next tool depends on the previous observation.
