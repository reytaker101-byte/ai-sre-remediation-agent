from dotenv import load_dotenv
from graph.main_graph import main_graph


def main():
    load_dotenv()
    print("=" * 78)
    print("AI PRODUCTION OPERATIONS & INCIDENT RESPONSE AGENT")
    print("=" * 78)

    incident = input("\nDescribe the incident: ").strip()
    if not incident:
        return

    result = main_graph.invoke({
        "incident": incident,
        "messages": [],
        "issues": [],
        "evidence": [],
    })

    print("\n" + result.get("final_report", "No report generated."))


if __name__ == "__main__":
    main()
