import json
import subprocess
from langchain_core.tools import tool


def _run(command: list[str], timeout: int = 20) -> str:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        output = result.stdout.strip() or result.stderr.strip()
        return output[:16000] if output else "(no output)"
    except FileNotFoundError:
        return f"Command not found: {command[0]}"
    except subprocess.TimeoutExpired:
        return f"Command timed out: {' '.join(command)}"


@tool
def docker_ps() -> str:
    """List Docker containers, names, status and ports."""
    return _run(["docker", "ps", "-a", "--no-trunc"])


@tool
def docker_logs(container: str, tail: int = 150) -> str:
    """Read recent logs from one Docker container."""
    return _run(["docker", "logs", "--tail", str(tail), container])


@tool
def docker_inspect(container: str) -> str:
    """Inspect one Docker container's runtime state and configuration."""
    return _run(["docker", "inspect", container])


@tool
def kubectl_get_pods(namespace: str = "") -> str:
    """List Kubernetes pods with namespace, readiness, status, restarts and node."""
    cmd = ["kubectl", "get", "pods"]
    cmd += ["-n", namespace] if namespace else ["-A"]
    cmd += ["-o", "wide"]
    return _run(cmd)


@tool
def kubectl_get_deployments(namespace: str = "") -> str:
    """List Kubernetes deployments and replica status."""
    cmd = ["kubectl", "get", "deployments"]
    cmd += ["-n", namespace] if namespace else ["-A"]
    return _run(cmd)


@tool
def kubectl_describe_pod(namespace: str, pod: str) -> str:
    """Describe an exact Kubernetes pod, including events and container state."""
    return _run(["kubectl", "describe", "pod", "-n", namespace, pod])


@tool
def kubectl_logs(namespace: str, pod: str, container: str = "") -> str:
    """Read recent logs from an exact Kubernetes pod/container."""
    cmd = ["kubectl", "logs", "-n", namespace, pod, "--tail", "150"]
    if container:
        cmd += ["-c", container]
    return _run(cmd)


@tool
def kubectl_get_events(namespace: str = "") -> str:
    """Read Kubernetes events. Read-only."""
    cmd = ["kubectl", "get", "events", "--sort-by=.lastTimestamp"]
    cmd += ["-n", namespace] if namespace else ["-A"]
    return _run(cmd)


@tool
def http_health_check(url: str) -> str:
    """GET an HTTP endpoint and return status and a response preview."""
    try:
        import requests
        response = requests.get(url, timeout=10)
        return json.dumps({
            "url": url,
            "status_code": response.status_code,
            "healthy": response.ok,
            "body_preview": response.text[:1200],
        }, indent=2)
    except Exception as exc:
        return f"Health check failed: {exc}"


READ_ONLY_TOOLS = [
    docker_ps, docker_logs, docker_inspect,
    kubectl_get_pods, kubectl_get_deployments,
    kubectl_describe_pod, kubectl_logs, kubectl_get_events,
    http_health_check,
]
