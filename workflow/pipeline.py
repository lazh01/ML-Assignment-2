from tools.open_alex import search_papers
from tools.filters import filter_papers
import json
import re

YEAR_FIELDS = {
    "publication_year",
    "in_year",
    "year",
    "min_year",
    "max_year",
    "before_year",
    "after_year",
}

CITATION_FIELDS = {
    "min_citations",
    "max_citations",
    "citation_count",
    "approximate_citations",
    "citations",
}

def parse_int(value):
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        value = value.strip()
        match = re.search(r"\d+", value)
        if match:
            return int(match.group())
    return None


def normalize_constraints(constraints):
    min_year = parse_int(constraints.get("min_year"))
    max_year = parse_int(constraints.get("max_year"))

    before_year = parse_int(constraints.get("before_year"))
    if before_year is not None:
        max_year = before_year - 1

    after_year = parse_int(constraints.get("after_year"))
    if after_year is not None:
        min_year = after_year + 1

    publication_year = parse_int(constraints.get("publication_year"))
    in_year = parse_int(constraints.get("in_year"))
    year = parse_int(constraints.get("year"))
    exact_year = publication_year if publication_year is not None else in_year if in_year is not None else year
    if exact_year is not None:
        min_year = exact_year
        max_year = exact_year

    if min_year is not None and max_year is not None and min_year > max_year:
        min_year, max_year = max_year, min_year

    min_citations = parse_int(constraints.get("min_citations"))
    max_citations = parse_int(constraints.get("max_citations"))
    citation_count = parse_int(constraints.get("citation_count"))
    approx_citations = parse_int(constraints.get("approximate_citations"))

    if citation_count is not None:
        if min_citations is None:
            min_citations = citation_count
        if max_citations is None:
            max_citations = citation_count

    if approx_citations is not None:
        delta = max(5, int(approx_citations * 0.1))
        if min_citations is None:
            min_citations = max(0, approx_citations - delta)
        if max_citations is None:
            max_citations = approx_citations + delta

    return min_year, max_year, min_citations, max_citations


def build_search_query(user_query, constraints):
    topic = constraints.get("topic") or ""
    other_terms = []

    for key, value in constraints.items():
        if not value:
            continue
        if key in {"topic", "min_year", "max_year", "publication_year", "in_year", "before_year", "after_year", "min_citations", "max_citations", "citation_count", "approximate_citations", "year"}:
            continue
        other_terms.append(str(value))

    if not topic:
        topic = user_query

    query_parts = [topic] + other_terms
    return " ".join(part for part in query_parts if part).strip()


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

    if not isinstance(constraints, dict):
        raise ValueError("Planner must return a JSON object with constraints.")

    topic = constraints.get("topic")
    min_year, max_year, min_citations, max_citations = normalize_constraints(constraints)
    search_query = build_search_query(user_query, constraints)

    print(f"Extracted Constraints: {constraints}")
    print(f"Search Query: {search_query}")
    print(f"Year range: {min_year} - {max_year}, Citations: {min_citations} - {max_citations}")

    # 2. Search (TOOL) using extracted constraints when possible
    papers = search_papers(
        search_query,
        min_year=min_year,
        max_year=max_year,
        min_citations=min_citations,
        max_citations=max_citations,
    )

    # 3. Filter (DETERMINISTIC) as a safety layer
    filtered = filter_papers(
        papers,
        min_year=min_year,
        max_year=max_year,
        min_citations=min_citations,
        max_citations=max_citations,
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