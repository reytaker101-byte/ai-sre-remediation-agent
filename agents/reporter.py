def build_report(state: dict) -> str:
    lines = [
        "=== INCIDENT REPORT ===",
        f"Incident: {state.get('incident', '')}",
        f"Route: {state.get('route', 'unknown')}",
        "",
        "=== OBSERVED ISSUES ===",
    ]

    issues = state.get("issues", [])
    for i, issue in enumerate(issues, 1):
        lines += [
            f"{i}. {issue.get('title', 'Unknown issue')}",
            f"   Severity: {issue.get('severity', 'unknown')}",
            f"   Resource: {issue.get('resource', 'unknown')}",
            f"   Namespace: {issue.get('namespace', 'unknown')}",
            f"   Impact: {issue.get('impact', 'unknown')}",
            "   Evidence:",
        ]
        lines += [f"     - {e}" for e in issue.get("evidence", [])]

    lines += [
        "",
        "=== ROOT CAUSE ===",
        state.get("root_cause", "Not established"),
        "",
        "=== REMEDIATION ===",
    ]
    lines += [f"- {x}" for x in state.get("remediation_steps", [])]
    lines += [
        "",
        f"Approval required: {state.get('approval_required', True)}",
        f"Approved: {state.get('approved', False)}",
        "",
        "=== VERIFICATION ===",
        state.get("verification_result", "Not performed"),
    ]
    return "\n".join(lines)
