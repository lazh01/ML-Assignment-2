from autogen import AssistantAgent
from config.llm_config import llm_config

planner = AssistantAgent(
    name="planner",
    llm_config=llm_config,
    system_message="""
Extract structured constraints from the user query.

Return only a single JSON object with zero or more of these keys:
- topic
- publication_year
- before_year
- after_year
- in_year
- min_year
- max_year
- min_citations
- max_citations
- approximate_citations
- citation_count
- author
- venue
- keywords

If the query asks for a specific year, use one of publication_year, in_year, before_year, or after_year.
If the query asks for citations loosely, use approximate_citations.
If it asks for a minimum or maximum citation count, use min_citations or max_citations.

Do not return any extra text, commentary, or explanation. Return valid JSON only.
"""
)