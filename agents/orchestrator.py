def route_incident(incident: str) -> str:
    text = incident.lower()
    if any(x in text for x in ["kubernetes", "pod", "deployment", "kubectl"]):
        return "kubernetes"
    if any(x in text for x in ["docker", "container"]):
        return "docker"
    return "application"
