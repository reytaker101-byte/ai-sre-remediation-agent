from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage

from state.schema import InvestigationState
from agents.investigator import build_investigator, system_message


def investigation_controller(state: InvestigationState):
    llm = build_investigator()
    messages = state.get("messages", [])

    if not messages:
        messages = [
            system_message(state.get("incident", "")),
            HumanMessage(content=state.get("incident", "")),
        ]

    response = llm.invoke(messages)

    return {
        "messages": [response],
        "evidence": state.get("evidence", []) + [response.content],
    }


builder = StateGraph(InvestigationState)
builder.add_node("investigation_controller", investigation_controller)
builder.add_edge(START, "investigation_controller")
builder.add_edge("investigation_controller", END)

investigation_subgraph = builder.compile()
