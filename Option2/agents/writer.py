from autogen import AssistantAgent
from Option2.config.llm_config import llm_config

writer = AssistantAgent(
    name="WriterAgent",
    llm_config=llm_config,
    system_message="""
Produce concise structured answers.

Include:
- title
- authors
- year
- citations
- citation source
- explanation

You are the final agent.

When you produce the final answer, you MUST end with:
TERMINATE

Do not call tools.
Do not ask questions.
"""
)