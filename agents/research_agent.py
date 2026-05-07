from autogen import AssistantAgent
from config.llm_config import llm_config

research_agent = AssistantAgent(
    name="research_agent",
    llm_config=llm_config,
    system_message="""
You are a research assistant.

Given candidate papers, choose ONE that best matches constraints. And also include explanations about any uncertainties as to its fit to the constraints and topic.

Return:
- title
- authors
- year
- citation count
- citation source
- link
- explanation
"""
)