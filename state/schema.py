from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class Issue(TypedDict, total=False):
    title: str
    severity: str
    resource: str
    namespace: str
    evidence: list[str]
    impact: str


class InvestigationState(TypedDict, total=False):
    incident: str
    route: str
    messages: Annotated[list[BaseMessage], add_messages]
    evidence: list[str]
    issues: list[Issue]
    root_cause: str
    root_cause_evidence: list[str]
    remediation_steps: list[str]
    approval_required: bool
    approved: bool
    verification_checks: list[str]
    verification_result: str
    resolved: bool
    final_report: str
