from autogen import AssistantAgent
from Option2.config.llm_config import llm_config

verifier = AssistantAgent(
    name="VerifierAgent",
    llm_config=llm_config,
    system_message="""
Verify:
- year constraints
- citation count
- topic relevance

Reject invalid papers.
"""
)