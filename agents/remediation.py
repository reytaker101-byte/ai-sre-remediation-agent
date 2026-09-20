def create_remediation_steps(issues: list, root_cause: str) -> list[str]:
    if not issues:
        return ["Do not change infrastructure until evidence is available."]

    steps = []
    for issue in issues:
        resource = issue.get("resource", "unknown")
        namespace = issue.get("namespace", "")
        target = f"{namespace}/{resource}" if namespace else resource
        steps.append(
            f"Target: {target}. Apply the smallest reversible change supported "
            "by the observed evidence."
        )
        steps.append(
            f"Verify {target} after the change using workload readiness, recent logs, "
            "health endpoint and error indicators."
        )
    return steps
