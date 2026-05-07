from autogen import AssistantAgent
from config.llm_config import llm_config

planner = AssistantAgent(
    name="planner",
    llm_config=llm_config,
    system_message="""
Extract structured constraints from the user query.

Return JSON with:
- topic
- min_year
- max_year
- min_citations

and make it so each is its own top-level item, so it can easily be used by other tools.
"""
)