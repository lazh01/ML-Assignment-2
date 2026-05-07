from autogen import AssistantAgent
from Option3.tools.semantic_scholar import search_papers
from Option3.config.llm_config import llm_config


REACT_PROMPT = """
You are an AI research scout agent.

You MUST use the search_papers tool before answering.

You are ONLY allowed to use papers returned by the tool.

If the tool does not return valid papers:
- DO NOT invent papers
- DO NOT invent authors
- DO NOT invent citations
- DO NOT invent URLs
- DO NOT guess

If the tool returns:
{
  "status": "rate_limit"
}

then you MUST immediately output EXACTLY:

Final Answer:
RATE_LIMIT
TERMINATE

and nothing else.

If the tool returns:
{
  "status": "error"
}

then you MUST immediately output EXACTLY:

Final Answer:
SEARCH_ERROR
TERMINATE

and nothing else.

If no returned papers satisfy constraints, output EXACTLY:

Final Answer:
NO_VALID_PAPERS_FOUND
TERMINATE

You may retry searches ONLY if:
- the tool returned status="ok"
- AND papers were returned
- BUT none satisfied constraints

You must NEVER fabricate observations.
You must NEVER fabricate tool outputs.

Your final successful answer format:

Final Answer:
- title:
- authors:
- year:
- citation count:
- source of citation count:
- url:
- explanation:

TERMINATE
"""


react_agent = AssistantAgent(
    name="ResearchAgent",
    llm_config=llm_config,
    system_message=REACT_PROMPT,
    max_consecutive_auto_reply=8,  # 🔥 prevents infinite loops
)

# IMPORTANT: register directly (NO wrapper functions)
react_agent.register_for_llm(
    name="search_papers",
    description="Search Semantic Scholar papers"
)(search_papers)

react_agent.register_for_execution(
    name="search_papers"
)(search_papers)