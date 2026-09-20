def build_structured_rca(issues: list, evidence: list) -> dict:
    if not issues:
        return {"root_cause": "Not established", "root_cause_evidence": []}

    issue = issues[0]
    return {
        "root_cause": issue.get("title", "Root cause not established"),
        "root_cause_evidence": issue.get("evidence", []),
    }
