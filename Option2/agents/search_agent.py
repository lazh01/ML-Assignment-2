from autogen import AssistantAgent
from Option2.config.llm_config import llm_config
from Option2.tools.semantic_scholar import search_papers

search_agent = AssistantAgent(
    name="SearchAgent",
    llm_config=llm_config,
    system_message="""
You search for research papers using available tools.
Only return real papers from tools.
"""
)

search_agent.register_for_llm(
    name="search_papers",
    description="Search Semantic Scholar for papers"
)(search_papers)

search_agent.register_for_execution(
    name="search_papers"
)(search_papers)