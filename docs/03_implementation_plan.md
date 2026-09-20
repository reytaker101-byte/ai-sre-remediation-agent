# Implementation plan

## Phase 1: Run the foundation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.main
```

## Phase 2: Docker

```bash
docker run -d --name demo-api nginx
docker ps -a
docker logs demo-api
docker inspect demo-api
docker stop demo-api
```

Ask the agent to investigate the stopped container.

## Phase 3: Kubernetes

Enable Kubernetes in Docker Desktop:

```bash
kubectl get nodes
kubectl get pods -A
```

Deploy a safe test workload and investigate it.

## Phase 4: Real tool-calling loop

Build:

```text
Investigation Controller
        ↓
LLM chooses tool
        ↓
tool executes
        ↓
result enters State
        ↓
LLM sees result
        ↓
another tool OR RCA
```

## Phase 5: Structured issue extraction

Every issue should contain:
- title
- severity
- resource
- namespace
- evidence
- impact

This is what prevents generic paragraphs.

## Phase 6: Resource-specific remediation

Every proposed action should include:
- resource type
- exact name
- namespace
- reason
- intended change
- risk
- verification

## Phase 7: Approval and execution

Only allowlisted actions should be executable.

Never give the LLM arbitrary production shell access.

## Phase 8: Verification and retry

```text
execute
  ↓
health
  ↓
logs
  ↓
metrics/smoke test
  ↓
resolved?
 /       yes       no
 |         |
report   investigate
```

## Phase 9: Multimodal

Accept:
- Grafana screenshots
- log files
- architecture diagrams
- incident PDFs

Extract evidence and add it to State.

## Phase 10: Production hardening

Add Kubernetes RBAC, policy engine, audit logs, secret management, approval service, rate limiting, persistent incident history, observability and evaluation.
