from agents.planner import planner
from agents.research_agent import research_agent
from workflow.pipeline import run_pipeline

if __name__ == "__main__":
    query = input("Enter your research query: ")

    result = run_pipeline(query, planner, research_agent)

    print("\nResult:\n")
    print(result)