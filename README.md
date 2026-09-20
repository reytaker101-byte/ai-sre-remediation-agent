# AI Production Operations & Autonomous Incident Response Agent

This project turns a conversational/tool-calling assistant pattern into a DevOps/SRE incident-response system.

## Goal

Given an incident such as:

> payment-api is returning 5xx errors. Investigate.

the system is designed to:
1. identify the affected service/resource;
2. investigate with live read-only Docker/Kubernetes/HTTP tools;
3. list concrete issues with evidence and resource names;
4. form an evidence-backed RCA hypothesis;
5. create resource-specific remediation steps;
6. require human approval before mutations;
7. execute only allowlisted remediation actions;
8. verify the result;
9. investigate again if the issue remains;
10. generate an incident report.

The starter is intentionally safe: mutation functions are approval-gated placeholders.

## Architecture

```text
USER / ALERT
      |
      v
INCIDENT ROUTER
      |
      v
INVESTIGATION SUBGRAPH
  |        |        |
Docker  Kubernetes  HTTP
tools     tools     health
  |        |        |
  +--------+--------+
           |
           v
       RCA / ISSUES
           |
           v
   RESOURCE-SPECIFIC
     REMEDIATION
           |
      HUMAN APPROVAL
           |
           v
       EXECUTE
           |
           v
        VERIFY
        /        resolved   not resolved
      |            |
      v            +--> investigate again
    REPORT
```

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.main
```

Docker Desktop and optional Docker Desktop Kubernetes are supported.

## Resume framing

Possible title:

**AI Autonomous DevOps Incident Response & Remediation Platform**

Only claim features that you actually implement and test.

Potential bullets after full implementation:
- Built a LangGraph-based incident-response platform using LLM-driven tool selection to investigate Docker/Kubernetes incidents iteratively.
- Implemented evidence-backed issue detection, resource-aware RCA and remediation planning with concrete namespace/workload/pod context.
- Added human-in-the-loop approval, allowlisted remediation actions and post-remediation verification.
- Implemented stateful orchestration, investigation subgraphs, tool-calling loops and conditional retry paths.
- Extended incident intake toward multimodal logs, screenshots and documents.
