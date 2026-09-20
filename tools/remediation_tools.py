from langchain_core.tools import tool


@tool
def restart_kubernetes_pod(namespace: str, pod: str) -> str:
    """Approval-gated restart of one exact pod. Disabled in starter."""
    return (
        f"APPROVED ACTION PLACEHOLDER: restart {namespace}/{pod}. "
        "No command executed. Add policy/RBAC/audit before enabling."
    )


@tool
def rollout_restart_deployment(namespace: str, deployment: str) -> str:
    """Approval-gated restart of one exact deployment. Disabled in starter."""
    return (
        f"APPROVED ACTION PLACEHOLDER: restart deployment "
        f"{namespace}/{deployment}. No command executed."
    )


APPROVED_REMEDIATION_TOOLS = [
    restart_kubernetes_pod,
    rollout_restart_deployment,
]
