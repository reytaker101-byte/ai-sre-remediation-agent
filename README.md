1. Project Goal
Build an AI-powered DevOps/SRE Incident Response Agent that can investigate live infrastructure, identify issues, perform evidence-based RCA, generate remediation plans, wait for human approval, execute approved remediation, and verify recovery.

2. Architecture
USER
  |
  v
INCIDENT ORCHESTRATOR
  |
  v
INVESTIGATION AGENT
  |---- Docker/Kubernetes read-only tools
  |
  v
ISSUE DETECTION
  |
  v
ROOT CAUSE ANALYSIS
  |
  v
REMEDIATION AGENT
  |
  v
HUMAN APPROVAL
  |
  v
EXECUTION
  |
  v
VERIFICATION
  |
  +---- Fixed ------> REPORT
  |
  +---- Not Fixed --> Investigation / retry path

3. Main Project Structure
ai-production-operations-agent-v2/
|
+-- agents/
|   +-- orchestrator.py
|   +-- investigator.py
|   +-- issue_detector.py
|   +-- rca.py
|   +-- remediation.py
|   +-- reporter.py
|
+-- app/
|   +-- main.py
|
+-- graph/
|   +-- investigation_subgraph.py
|   +-- main_graph.py
|
+-- state/
|   +-- schema.py
|
+-- tools/
|   +-- ops_tools.py
|   +-- remediation_tools.py
|
+-- docs/
|   +-- 01_use_case.md
|   +-- 02_topics.md
|   +-- 03_implementation_plan.md
|
+-- tests/
+-- Dockerfile
+-- docker-compose.yml
+-- requirements.txt
+-- README.md
+-- .env.example

4. Virtual Environment
Command:
python3 -m venv .venv

Purpose:
Creates an isolated Python environment for the project.

Activate:
source .venv/bin/activate

Expected terminal:
(.venv) admin@NewLearning#

5. Install Dependencies
Command:
pip install -r requirements.txt

Purpose:
Installs LangGraph, LangChain, OpenAI integration, dotenv, requests and other project dependencies.

6. OpenAI API Configuration
The project uses an environment variable for the OpenAI API key.

.env:
OPENAI_API_KEY=...

Important:
Never commit .env to GitHub.

.env.example should contain:
OPENAI_API_KEY=

7. Docker Test Container
Example container:
demo-api

Create/run:
docker run -d --name demo-api -p 8080:80 nginx

Stop:
docker stop demo-api

Check all containers:
docker ps -a

Check running containers:
docker ps

Start:
docker start demo-api

Purpose:
demo-api is the live infrastructure target used to test the AI incident-response workflow.

8. Application Start
Run from project root:

python -m app.main

The application asks:

Describe the incident:

Example:
Docker container demo-api is stopped and the application is unavailable.

The incident is then passed into the LangGraph workflow.

9. LangGraph Main Workflow
main_graph.py creates the main workflow.

Flow:

START
  |
route
  |
investigation
  |
issue_detection
  |
rca
  |
remediation
  |
human_approval
  |
execution
  |
verify
  |
report
  |
END

Each node performs one responsibility.

10. State
state/schema.py defines the shared workflow state.

State is like an "incident notebook".

It stores:
- incident
- investigation_round
- messages
- evidence
- issues
- root_cause
- root_cause_evidence
- root_cause_confidence
- remediation_steps
- approval_required
- approved
- execution_result
- verification_checks
- verification_result
- resolved
- final_report

Every graph node can read/update this shared state.

11. Orchestrator
agents/orchestrator.py decides how the incident should be handled.

The orchestrator receives the incident description and determines the appropriate incident route.

The important point:
The workflow is not simply a fixed chatbot response. The incident is passed through an agentic workflow where tools and evidence are used during investigation.

12. Investigation Agent
agents/investigator.py contains the investigation agent.

It uses:

ChatOpenAI
+
read-only Docker/Kubernetes tools

The LLM decides which investigation tools are relevant.

Rules:
- Investigate before RCA.
- Never invent evidence.
- Never modify infrastructure.
- Use read-only tools.
- Continue investigation when evidence is insufficient.
- Prefer exact resource-specific investigation.

13. Read-Only Operations Tools
tools/ops_tools.py provides live infrastructure tools.

Docker:
docker_ps()
docker_logs(container)
docker_inspect(container)

Kubernetes:
kubectl_get_pods()
kubectl_get_deployments()
kubectl_describe_pod(namespace, pod)
kubectl_logs(namespace, pod)
kubectl_get_events(namespace)

HTTP:
http_health_check(url)

These tools execute real Docker/Kubernetes/HTTP commands and return their output to the agent.

14. Investigation Subgraph
graph/investigation_subgraph.py contains a smaller LangGraph workflow.

It handles:

LLM investigation
      |
      v
Tool selection
      |
      v
Tool execution
      |
      v
Investigation policy
      |
      v
Additional evidence collection
      |
      v
Evidence extraction

A subgraph is basically a complete smaller workflow inside the main workflow.

15. Tool Calling
The investigator is bound to the read-only tools.

Example:

LLM
 |
 | decides evidence is needed
 v
docker_ps()
 |
 v
Docker output
 |
 v
LLM receives result
 |
 | decides more evidence is needed
 v
docker_inspect()
 |
 v
Docker output
 |
 v
docker_logs()

This is the important agentic behavior:
The LLM can decide what evidence it needs instead of only receiving pre-written logs.

16. Evidence Collection
Tool outputs are collected into:

state["evidence"]

Example evidence:

Container demo-api:
Status: Exited
ExitCode: 0
Running: false

The system uses actual command output rather than assuming the problem.

17. Issue Detection
agents/issue_detector.py analyzes the collected evidence.

It identifies concrete issues.

Example:

Issue:
Docker container demo-api is stopped.

Severity:
High

Resource:
demo-api

Evidence:
Container state shows Exited and Running=false.

Impact:
Application availability is affected if this container provides the application service.

The issue detector must not invent:
- resource names
- metrics
- errors
- restart counts
- configuration
- causes

18. Root Cause Analysis
agents/rca.py performs evidence-based RCA.

The RCA agent receives:

Issues
+
Evidence

It returns:

root_cause
root_cause_evidence
root_cause_confidence

Important rule:

If evidence is insufficient:

"Root cause not established from available evidence."

This prevents the LLM from hallucinating a root cause.

19. Remediation Planning
agents/remediation.py creates a remediation plan.

Each remediation step contains:

Action
Target
Reason
Risk
Rollback
Verification

Example:

Action:
Start Docker container

Target:
demo-api

Reason:
Container is confirmed stopped.

Risk:
Service startup may fail if an underlying application issue exists.

Rollback:
Stop the container if required.

Verification:
Check Docker running state and application health.

20. Human Approval
Before infrastructure mutation, the workflow pauses for human approval.

Example:

HUMAN APPROVAL REQUIRED

Proposed remediation:

1. Action: Start Docker container
   Target: demo-api
   Reason: Container is stopped
   Risk: Application may fail during startup
   Rollback: Stop container if required

Approve remediation?
Type YES to execute.

Only "YES" allows execution.

21. Remediation Execution + Safety
tools/remediation_tools.py contains mutation tools.

Current Docker actions include:

docker_start()
docker_restart()
docker_stop()

The current workflow uses:

docker start demo-api

There is also an allowlist check.

If the generated target is not allowlisted:

Execution blocked.

This provides a safety layer so the LLM cannot freely execute arbitrary infrastructure commands.

22. Post-Remediation Verification
After execution, the workflow verifies whether the infrastructure actually recovered.

For demo-api:

docker inspect demo-api

The system checks:

"Running": true

If true:

SUCCESS:
demo-api is running after remediation.

If false:

FAILED:
demo-api is still not running after remediation.

The final report contains:
- Detected issues
- Evidence
- RCA
- Remediation plan
- Approval status
- Execution result
- Verification result
- Resolution status

Key interview explanation:

"I built an AI-driven DevOps incident-response agent using LangGraph that investigates live Docker/Kubernetes infrastructure through tool calling, performs evidence-backed issue detection and RCA, generates resource-specific remediation plans, waits for human approval before making changes, executes the approved remediation, and verifies whether the service actually recovered."
