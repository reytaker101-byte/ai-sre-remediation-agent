1. Project Overview

AI DevOps Incident Response Agent is an AI-powered SRE/DevOps incident investigation and remediation platform built using LangGraph, LangChain, OpenAI, Docker and Python.

The agent investigates live infrastructure instead of relying only on manually pasted logs. It uses read-only Docker/Kubernetes tools to collect evidence, identifies operational issues, performs evidence-based Root Cause Analysis (RCA), generates a resource-specific remediation plan, asks for human approval before making infrastructure changes, executes the approved remediation, and verifies whether the service has recovered.


2. Problem Statement

Traditional incident analysis often requires an engineer to manually:

- Check container or Kubernetes status
- Inspect failed resources
- Read application logs
- Identify the root cause
- Decide remediation steps
- Execute the fix
- Verify service recovery

This project demonstrates how an AI agent can perform these investigation steps dynamically using live infrastructure tools and maintain state throughout the incident workflow.


3. Project Goal

The goal is to build an AI-driven DevOps/SRE agent that can:

- Understand an incident description
- Investigate live infrastructure
- Select appropriate investigation tools
- Collect evidence
- Detect concrete operational issues
- Perform evidence-backed RCA
- Generate exact remediation steps
- Request human approval before infrastructure changes
- Execute approved remediation
- Verify service recovery
- Generate a final incident report


4. High-Level Architecture

USER
  |
  v
INCIDENT ORCHESTRATOR
  |
  v
INVESTIGATION SUBGRAPH
  |
  +--> Docker/Kubernetes Read-Only Tools
  |
  +--> Evidence Collection
  |
  v
ISSUE DETECTION
  |
  v
ROOT CAUSE ANALYSIS
  |
  v
REMEDIATION PLANNING
  |
  v
HUMAN APPROVAL
  |
  +--> REJECT --> Report
  |
  +--> APPROVE
          |
          v
     REMEDIATION EXECUTION
          |
          v
       VERIFICATION
          |
          +--> RESOLVED --> Report
          |
          +--> NOT RESOLVED --> Further Investigation


5. Technology Stack

- Python
- LangGraph
- LangChain
- LangChain OpenAI
- OpenAI GPT-5-mini
- Docker
- Kubernetes / kubectl
- Pydantic
- Requests
- python-dotenv
- Docker Compose
- Git / GitHub


6. Project Structure

ai-devops-incident-response-agent/
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
|   +-- test_placeholder.py
|
+-- Dockerfile
+-- docker-compose.yml
+-- requirements.txt
+-- .env.example
+-- README.md


7. Virtual Environment

A Python virtual environment is used to isolate project dependencies.

Create the environment:

python3 -m venv .venv

Activate it:

source .venv/bin/activate

After activation, the terminal should show:

(.venv)


8. Install Dependencies

Install the required Python packages:

pip install -r requirements.txt

The requirements include packages required for:

- LangGraph
- LangChain
- OpenAI integration
- Pydantic
- Requests
- Environment variable handling


9. Environment Configuration

The application uses environment variables for configuration.

Create the environment file:

cp .env.example .env

The OpenAI API key is loaded from the environment.

The application uses:

load_dotenv()

This loads values from the .env file into the Python environment.

IMPORTANT:

Never commit the real OpenAI API key to GitHub.

Example:

export OPENAI_API_KEY="YOUR_API_KEY"

Do not put the actual API key in README.md, source code or Git history.


10. Docker Test Environment

The project uses a Docker container as a simple incident target.

Example container:

demo-api

The container uses the nginx image.

Check running containers:

docker ps

Example when no container is running:

CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

Check all containers, including stopped containers:

docker ps -a

Example:

CONTAINER ID   IMAGE     COMMAND                  CREATED       STATUS                        PORTS     NAMES
2aa34256894e   nginx     "/docker-entrypoint..."   3 hours ago   Exited (255) 20 seconds ago   80/tcp    demo-api

The important difference is:

docker ps
- Shows only running containers.

docker ps -a
- Shows both running and stopped/exited containers.


11. Starting the Demo Container

The container can be started manually using:

docker container start 2aa

Example output:

2aa

The same container can also be started using its name:

docker start demo-api

Example output:

demo-api

For incident testing, the container can be stopped:

docker stop demo-api

Example output:

demo-api

After stopping it:

docker ps

Output:

CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

The container does not appear because docker ps only displays running containers.

Check again with:

docker ps -a

The stopped container appears with an Exited status.


12. Project Directory and Virtual Environment

The project must be executed from the project root.

Example:

cd Desktop/ai-production-operations-agent-v2

Activate the virtual environment:

source .venv/bin/activate

Expected prompt:

(.venv) admin@NewLearning#

If the command is executed from the wrong directory:

source .venv/bin/activate

may return:

source: no such file or directory: .venv/bin/activate

This happens because .venv exists inside the project directory, not necessarily in the current directory.

Check the current directory:

pwd

Example:

/Users/dollyd/Desktop/ai-production-operations-agent-v2


13. Python Import Validation

The project contains a Python package named graph.

The import test is:

python -c "from graph.main_graph import main_graph; print('FINAL GRAPH OK')"

This command should be executed from the project root.

Correct result:

FINAL GRAPH OK

If executed from inside the graph directory:

cd graph

then running the same command can fail with:

ModuleNotFoundError: No module named 'graph'

The reason is that Python is now running from inside the package directory rather than its parent project directory.

Return to the project root:

cd ..

Then run:

python -c "from graph.main_graph import main_graph; print('FINAL GRAPH OK')"

Expected output:

FINAL GRAPH OK


14. Running the Application

Start the application from the project root:

python -m app.main

The application displays:

==============================================================================
AI PRODUCTION OPERATIONS & INCIDENT RESPONSE AGENT
==============================================================================

Then enter an incident description.

Example:

The demo-api Docker container is unavailable. Investigate the incident using live Docker evidence, identify the actual issue, determine the root cause only if supported by evidence, and create a precise remediation plan requiring human approval.

The agent then starts the LangGraph workflow.


15. Main LangGraph Workflow

The main workflow is implemented in:

graph/main_graph.py

The workflow contains these major stages:

1. Route the incident
2. Investigate the infrastructure
3. Detect issues
4. Perform RCA
5. Generate remediation plan
6. Ask for human approval
7. Execute approved remediation
8. Verify recovery
9. Generate final report

The workflow is stateful, meaning each stage receives information produced by previous stages.


16. Shared State

The shared state is defined in:

state/schema.py

The state acts like a shared incident notebook.

It stores information such as:

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

This allows different agents and graph nodes to work on the same incident context.


17. Investigation Agent

The investigation agent is implemented in:

agents/investigator.py

Its job is to investigate the incident using live read-only tools.

The agent is instructed to:

- Investigate before reaching RCA
- Never invent evidence
- Never modify infrastructure
- Use read-only tools
- Continue investigating when evidence is insufficient
- Prefer exact resource-specific investigation

The investigation agent uses LLM tool calling to decide which investigation tools should be used.


18. Read-Only Operations Tools

Read-only infrastructure tools are implemented in:

tools/ops_tools.py

Docker tools:

docker_ps()
- Lists Docker containers
- Shows container status
- Shows ports and container names

docker_logs()
- Retrieves recent container logs

docker_inspect()
- Retrieves detailed Docker container configuration and runtime state

Kubernetes tools:

kubectl_get_pods()
- Lists Kubernetes pods

kubectl_get_deployments()
- Lists Kubernetes deployments

kubectl_describe_pod()
- Describes an exact Kubernetes pod
- Includes events and container state

kubectl_logs()
- Retrieves logs from a Kubernetes pod

kubectl_get_events()
- Retrieves Kubernetes events

HTTP tool:

http_health_check()
- Performs an HTTP GET request
- Returns status code
- Indicates whether the endpoint is healthy
- Provides a response preview

These tools are read-only and are intended for investigation.


19. Investigation Subgraph

The investigation workflow is implemented in:

graph/investigation_subgraph.py

A subgraph is a smaller LangGraph workflow embedded inside the main graph.

The investigation subgraph handles:

- LLM-based investigation
- Tool calling
- Tool execution
- Evidence collection
- Investigation policy
- Investigation rounds

The basic flow is:

START
  |
  v
Investigation Controller
  |
  v
Tool Selection
  |
  v
Tool Execution
  |
  v
Investigation Policy
  |
  +--> Continue Investigation
  |
  +--> Forced Evidence Collection
  |
  +--> Extract Evidence
  |
  v
END

The subgraph also contains a safety guardrail that ensures important Docker evidence is collected for the demo incident.


20. Issue Detection

Issue detection is implemented in:

agents/issue_detector.py

The issue detector analyzes collected evidence and identifies concrete operational problems.

Each issue can contain:

- Title
- Severity
- Exact resource
- Namespace
- Evidence
- Impact

Example:

Issue:
Docker container 'demo-api' is stopped (Exited)

Severity:
High

Resource:
demo-api

Evidence:
Container state shows Exited

Impact:
The demo-api container is not running and the service is unavailable.

Important rule:

The issue detector must not invent information that is not present in the evidence.

For example, if evidence only shows that a container is stopped, it must not automatically claim that the application crashed.


21. Root Cause Analysis

RCA is implemented in:

agents/rca.py

The RCA agent analyzes:

- Detected issues
- Collected evidence

It produces:

- Root cause
- Root cause evidence
- Root cause confidence

The RCA agent is explicitly instructed to use only supplied evidence.

In the demonstrated run, the agent correctly returned:

Root cause not established from available evidence.

This is important because an exited container does not automatically prove why the container stopped.

The system therefore distinguishes an observed fact from an unproven hypothesis.


22. Remediation Planning

Remediation planning is implemented in:

agents/remediation.py

The remediation agent generates precise remediation steps based on:

- Issues
- Root cause
- Evidence

Each remediation step contains:

- Action
- Exact target
- Reason
- Risk
- Rollback
- Verification checks

The agent is instructed to:

- Never invent resource names
- Never invent namespaces
- Prefer the smallest reversible change
- Explain why the action is supported by evidence
- Include operational risk
- Include rollback
- Include verification

If evidence is insufficient to safely remediate the problem, the agent can return no remediation steps.

In the demonstrated run, the generated remediation plan included:

1. Collect runtime logs for demo-api
2. Inspect container metadata and last state
3. Attempt the smallest restorative action using docker start demo-api
4. Consider a restart policy only if supported by inspection and operator intent
5. Escalate for further troubleshooting if the container cannot be started reliably

The plan also identified the exact Docker container:

demo-api

Container ID:

2aa34256894e25744ebd89fdb80dc4d2bbf10cbc6c5a7ff5d826696652376173


23. Human Approval

Infrastructure changes are not executed automatically.

The workflow reaches a human approval node before remediation.

The user is shown:

- Proposed action
- Target
- Reason
- Risk
- Rollback

Example output:

==============================================================================
HUMAN APPROVAL REQUIRED
==============================================================================

Proposed remediation:

1. Action : Collect runtime logs for the container
   Target : Container demo-api
   Reason : Evidence shows the container is exited
   Risk   : Low - read-only
   Rollback: None required

2. Action : Inspect the container metadata and last state
   Target : Container demo-api
   Reason : Confirm exit code, finished time, OOM status and restart policy
   Risk   : Low - read-only
   Rollback: None required

3. Action : Attempt the smallest restorative action:
   docker start demo-api
   Target : Container demo-api
   Reason : The container exists and is exited
   Risk   : Medium
   Rollback: docker stop demo-api

The application then asks:

Approve remediation? Type YES to execute, anything else to reject:

Only typing:

YES

allows the remediation execution stage to proceed.

Any other response rejects the remediation.

This creates a Human-in-the-Loop safety mechanism.


24. Remediation Execution

Remediation execution is implemented in:

tools/remediation_tools.py

and the execution logic is handled by:

graph/main_graph.py

The current demo supports Docker actions such as:

docker_start()
docker_restart()
docker_stop()

For the demonstrated incident, the approved remediation executed:

docker start demo-api

Execution output:

==============================================================================
EXECUTING APPROVED REMEDIATION
==============================================================================

Action : Start Docker container
Target : demo-api

Execution result: docker start demo-api -> demo-api

The allowlist check prevents the demo execution layer from blindly modifying arbitrary resources.


25. Post-Remediation Verification

After remediation, the agent verifies whether the service actually recovered.

The verification stage uses:

docker inspect demo-api

It checks the container's Running state.

Successful verification output:

==============================================================================
POST-REMEDIATION VERIFICATION
==============================================================================

SUCCESS: demo-api is running after remediation.

The system then confirms the running container:

docker ps

Output:

CONTAINER ID   IMAGE     COMMAND                  CREATED       STATUS              PORTS     NAMES
2aa34256894e   nginx     "/docker-entrypoint..."   3 hours ago   Up About a minute   80/tcp    demo-api

This confirms that the container is running after the approved remediation.


26. Complete End-to-End Demonstration

The following sequence demonstrates the complete incident lifecycle.

Step 1 - Check running containers:

docker ps

Output:

CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES


Step 2 - Check all containers:

docker ps -a

Output:

CONTAINER ID   IMAGE     COMMAND                  CREATED       STATUS                        PORTS     NAMES
2aa34256894e   nginx     "/docker-entrypoint..."   3 hours ago   Exited (255) 20 seconds ago   80/tcp    demo-api


Step 3 - Stop the demo container to simulate an incident:

docker stop demo-api

Output:

demo-api


Step 4 - Activate the project virtual environment:

cd Desktop/ai-production-operations-agent-v2

source .venv/bin/activate

Expected:

(.venv) admin@NewLearning#


Step 5 - Verify the project root:

pwd

Output:

/Users/dollyd/Desktop/ai-production-operations-agent-v2


Step 6 - Validate the LangGraph application import:

python -c "from graph.main_graph import main_graph; print('FINAL GRAPH OK')"

Output:

FINAL GRAPH OK


Step 7 - Start the AI incident-response agent:

python -m app.main


Step 8 - Provide the incident:

The demo-api Docker container is unavailable. Investigate the incident using live Docker evidence, identify the actual issue, determine the root cause only if supported by evidence, and create a precise remediation plan requiring human approval.


Step 9 - AI investigation identifies the observed issue:

Docker container 'demo-api' is stopped (Exited)

Severity:

High

Resource:

demo-api

Evidence:

CONTAINER ID                                                       IMAGE
2aa34256894e25744ebd89fdb80dc4d2bbf10cbc6c5a7ff5d826696652376173   nginx

Status:

Exited (0)

Impact:

The demo-api container is not running and the service is unavailable.


Step 10 - RCA:

Root cause not established from available evidence.

This demonstrates that the agent does not automatically convert an observed stopped state into an unsupported root-cause claim.


Step 11 - AI generates a remediation plan.

The plan identifies:

- Exact target resource
- Proposed action
- Reason
- Risk
- Rollback
- Verification


Step 12 - Human approval:

Approve remediation? Type YES to execute, anything else to reject:

User response:

YES


Step 13 - Approved remediation executes:

Action : Start Docker container
Target : demo-api

Execution result:

docker start demo-api -> demo-api


Step 14 - Post-remediation verification:

SUCCESS: demo-api is running after remediation.


Step 15 - Final Docker validation:

docker ps

Output:

CONTAINER ID   IMAGE     COMMAND                  CREATED       STATUS              PORTS     NAMES
2aa34256894e   nginx     "/docker-entrypoint..."   3 hours ago   Up About a minute   80/tcp    demo-api


Step 16 - Final incident result:

=== INCIDENT REPORT ===

Incident:
The demo-api Docker container is unavailable.

=== OBSERVED ISSUES ===

1. Docker container 'demo-api' is stopped (Exited)

Severity:
High

Resource:
demo-api

Impact:
The demo-api container is not running and the demo-api service is unavailable.

Evidence:
Container status shows Exited.


=== ROOT CAUSE ===

Root cause not established from available evidence.


=== REMEDIATION ===

The AI generated a resource-specific remediation plan including:

- Log collection
- Container inspection
- Starting the existing container
- Conditional restart-policy consideration
- Escalation if the container fails again


Approval required:

True

Approved:

True


=== VERIFICATION ===

SUCCESS: demo-api is running after remediation.


27. Closed-Loop Incident Response

The complete system follows this closed-loop pattern:

INVESTIGATE
    |
    v
COLLECT LIVE EVIDENCE
    |
    v
IDENTIFY ISSUE
    |
    v
PERFORM RCA
    |
    v
GENERATE REMEDIATION PLAN
    |
    v
HUMAN APPROVAL
    |
    +---- REJECT ----> REPORT
    |
    +---- APPROVE
             |
             v
        EXECUTE CHANGE
             |
             v
          VERIFY
             |
             +---- RESOLVED ----> REPORT
             |
             +---- NOT RESOLVED
                       |
                       v
                FURTHER INVESTIGATION

The important design principle is that the agent does not consider the incident fixed merely because a remediation command was executed.

It verifies the actual infrastructure state after the change.


28. Safety Controls

The project includes several safety controls:

- Read-only tools for investigation
- Human approval before mutation
- Exact resource targeting
- Evidence-backed issue detection
- Evidence-backed RCA
- Remediation risk description
- Rollback guidance
- Allowlisted remediation target
- Post-remediation verification
- No automatic claim of root cause when evidence is insufficient
- No destructive recreate/delete operation without confirmed analysis


29. Example Incident Lifecycle

Example incident:

demo-api Docker container is unavailable.

Observed evidence:

demo-api exists but is in Exited state.

AI issue detection:

Container demo-api is stopped.

RCA:

Root cause not established from available evidence.

Remediation:

Start the existing container after human approval.

Execution:

docker start demo-api

Verification:

docker inspect demo-api

Result:

Running = true

Final status:

Incident resolved.


30. Key AI/Agentic Concepts Demonstrated

This project demonstrates practical use of:

- LLM tool calling
- Agentic investigation
- LangGraph state management
- LangGraph subgraphs
- Conditional routing
- Tool execution
- Structured LLM output
- Pydantic schemas
- Evidence-based RCA
- Human-in-the-loop approval
- Safe infrastructure mutation
- Closed-loop verification
- Stateful incident workflows
- DevOps/SRE automation
- Docker operations
- Kubernetes investigation tooling


31. What Makes This Different From a Simple Chatbot

A traditional chatbot may receive logs and generate a paragraph describing the problem.

This project instead interacts with live infrastructure.

The agent can:

1. Receive an incident description
2. Select investigation tools
3. Query Docker/Kubernetes
4. Collect actual runtime evidence
5. Identify concrete issues
6. Perform RCA using the collected evidence
7. Generate a resource-specific remediation plan
8. Wait for human approval
9. Execute the approved infrastructure action
10. Verify the actual infrastructure state
11. Generate the final incident report

The key difference is:

The AI is connected to operational tools and participates in an executable incident-response workflow instead of only generating text.


32. Resume Project Description

Project:

AI DevOps Incident Response Agent

Description:

Built a LangGraph-based AI DevOps/SRE incident-response platform that investigates live Docker/Kubernetes infrastructure using LLM-driven tool calling, performs evidence-backed issue detection and RCA, generates resource-specific remediation plans, requires human approval for infrastructure mutations, and validates service recovery through post-remediation verification.


33. Interview One-Liner

"I built an AI SRE agent that doesn't just analyze pasted logs and generate a paragraph. It investigates live infrastructure using tools, collects evidence, performs evidence-backed RCA, proposes a remediation, waits for human approval, executes the approved change, and verifies whether the service actually recovered."


34. Important Project Limitation

The current implementation is a working demonstration focused on Docker incident response.

The current demo includes:

- Docker investigation
- Docker remediation
- Human approval
- Post-remediation verification
- Kubernetes read-only investigation tools

The Kubernetes tools are included in the project, but the demonstrated end-to-end remediation workflow was tested against the Docker demo container.

The current demo also contains a deterministic safety guardrail for the demo target "demo-api".

Future production extensions can include:

- Generic Kubernetes remediation
- Multiple incident types
- Kubernetes deployment rollback
- Pod restart/remediation
- Prometheus metrics
- Grafana integration
- Cloud infrastructure investigation
- Slack/PagerDuty integration
- Persistent incident memory
- Approval through Slack/Teams
- Automated retry investigation after failed remediation
- Multi-service dependency analysis
- Audit logging
- RBAC-based remediation permissions
