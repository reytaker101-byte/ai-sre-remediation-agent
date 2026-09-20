# Beginner-friendly concepts

## LLM
The language/reasoning engine. It reads the incident and tool results and decides what information is useful next. It does not know live cluster state by itself.

## Agent
An LLM with instructions, tools, state and a loop that lets it take actions toward a goal.

A useful mental model:

```text
LLM + Tools + State + Loop = Agent
```

## Tool
A controlled function that interacts with the environment.

Examples:
- docker_ps
- docker_logs
- kubectl_get_pods
- kubectl_describe_pod
- kubectl_logs
- http_health_check

## LangGraph
The workflow/orchestration layer. It defines state, nodes, edges, loops, subgraphs and approval points.

## State
The shared incident notebook:
incident, messages, evidence, issues, RCA, remediation and verification.

## Node
One workflow step, such as route, investigate, RCA, remediate, verify or report.

## Edge
Defines what runs next.

## Subgraph
A smaller complete graph used inside the main graph.

```text
Main graph
  |
  +--> Investigation subgraph
  |       +--> tools
  |       +--> evidence
  |       +--> RCA
  |
  +--> Remediation
```

## Multi-agent
Multiple specialized agents cooperate, for example:
Orchestrator -> Investigator -> RCA -> Remediator -> Reporter.

Benefit: clear responsibility boundaries and independently evolvable specialists.

## Multimodal
The agent can use different input types: alert text, logs, screenshots, diagrams, PDFs or audio where supported.

For SRE this could mean:
Grafana screenshot + incident text + log file -> common incident state.

Multimodal is an extension; it is not required for the first MVP.

## Human-in-the-loop
The agent investigates and proposes an exact action, but a human approves a risky mutation.

## Verification
After a change, check health, logs, workload state, smoke tests and metrics. If the incident remains, return to investigation.
