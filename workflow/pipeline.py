from tools.open_alex import search_papers
from tools.filters import filter_papers
import json

def run_pipeline(user_query, planner, research_agent):
    
    # 1. Extract constraints (LLM)
    plan = planner.generate_reply(
        messages=[{"role": "user", "content": user_query}]
    )

    plan = plan["content"]
    if isinstance(plan, str):
        constraints = json.loads(plan)
    else:
        constraints = plan

    topic = constraints.get("topic")
    min_year = constraints.get("min_year")
    max_year = constraints.get("max_year")
    min_citations = constraints.get("min_citations")
    print(f"Extracted Constraints: {constraints}")
    print(f"Extracted Topic: {topic}, Min Year: {min_year}, Max Year: {max_year}, Min Citations: {min_citations}")
    # 2. Search (TOOL)
    papers = search_papers(topic)

    # 3. Filter (DETERMINISTIC)
    filtered = filter_papers(
        papers,
        min_year=min_year,
        max_year=max_year,
        min_citations=min_citations
    )

    if not filtered:
        return "No papers found matching constraints."

    # 4. Let LLM pick best
    response = research_agent.generate_reply(
        messages=[{
            "role": "user",
            "content": f"Candidates: {filtered}, constraints: {constraints}, topic: {topic}"
        }]
    )

    return response