from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from tools.ops_tools import READ_ONLY_TOOLS


SYSTEM_PROMPT = """
You are a DevOps/SRE investigation agent.

Investigate with read-only tools and produce concrete operational findings.

Rules:
- Discover exact service/resource names where possible.
- Do not invent names, metrics or causes.
- Use tools to gather evidence.
- After every tool result, reassess what should be checked next.
- Keep observed issues separate from hypotheses.
- For each issue include resource, namespace when relevant, evidence and impact.
- End with the most likely RCA and the evidence supporting it.
- Never mutate infrastructure.
"""


def build_investigator():
    model = ChatOpenAI(model=None, temperature=0)
    return model.bind_tools(READ_ONLY_TOOLS)


def system_message(incident: str):
    return SystemMessage(content=SYSTEM_PROMPT + f"\nIncident:\n{incident}")
