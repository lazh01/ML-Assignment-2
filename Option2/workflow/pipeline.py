from Option2.agents.planner import planner
from Option2.agents.search_agent import search_agent
from Option2.agents.verifier import verifier
from Option2.agents.writer import writer
from autogen import GroupChat, UserProxyAgent, GroupChatManager
from Option2.config.llm_config import llm_config

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config=False
)

groupchat = GroupChat(
    agents=[
        planner,
        search_agent,
        verifier,
        writer
    ],
    messages=[],
    max_round=10,
    speaker_selection_method="round_robin"
)

def is_termination(msg):
    return (
        msg.get("content") is not None
        and "TERMINATE" in msg["content"]
    )

manager = GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config,
    is_termination_msg=is_termination
)