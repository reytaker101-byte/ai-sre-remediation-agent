from langgraph.graph import StateGraph, START, END

from state.schema import InvestigationState
from graph.investigation_subgraph import investigation_subgraph
from agents.orchestrator import route_incident
from agents.rca import build_structured_rca
from agents.remediation import create_remediation_steps
from agents.reporter import build_report


def route_node(state: InvestigationState):
    return {"route": route_incident(state.get("incident", ""))}


def rca_node(state: InvestigationState):
    return build_structured_rca(
        state.get("issues", []),
        state.get("evidence", []),
    )


def remediation_node(state: InvestigationState):
    return {
        "remediation_steps": create_remediation_steps(
            state.get("issues", []),
            state.get("root_cause", ""),
        ),
        "approval_required": True,
    }


def verification_node(state: InvestigationState):
    return {
        "verification_result": (
            "Verification stage reached. No mutation was executed by the starter."
        ),
        "resolved": False,
    }


def report_node(state: InvestigationState):
    return {"final_report": build_report(state)}


builder = StateGraph(InvestigationState)
builder.add_node("route", route_node)
builder.add_node("investigation", investigation_subgraph)
builder.add_node("rca", rca_node)
builder.add_node("remediation", remediation_node)
builder.add_node("verify", verification_node)
builder.add_node("report", report_node)

builder.add_edge(START, "route")
builder.add_edge("route", "investigation")
builder.add_edge("investigation", "rca")
builder.add_edge("rca", "remediation")
builder.add_edge("remediation", "verify")
builder.add_edge("verify", "report")
builder.add_edge("report", END)

main_graph = builder.compile()
