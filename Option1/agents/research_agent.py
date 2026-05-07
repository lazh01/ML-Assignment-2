from autogen import AssistantAgent
from Option1.config.llm_config import llm_config

research_agent = AssistantAgent(
    name="research_agent",
    llm_config=llm_config,
    system_message="""
You are a research assistant.

Given candidate papers, choose ONE that best matches constraints.

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