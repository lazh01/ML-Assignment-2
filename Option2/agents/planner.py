from autogen import AssistantAgent
from Option2.config.llm_config import llm_config

planner = AssistantAgent(
    name="Planner",
    llm_config=llm_config,
    system_message="""
You extract constraints and coordinate the search.

Delegate paper searching to SearchAgent.
Delegate validation to VerifierAgent.
Delegate summarization to WriterAgent.
"""
)