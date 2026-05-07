from autogen import UserProxyAgent
from Option3.agents.react_agent import react_agent
from Option3.tools.semantic_scholar import search_papers


user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config=False,
    function_map={
        "search_papers": search_papers
    },
    is_termination_msg=lambda msg: (
        isinstance(msg, dict)
        and isinstance(msg.get("content"), str)
        and (
            msg["content"].strip().endswith("TERMINATE")
        )
    )
)


if __name__ == "__main__":
    query = input("Enter your research query:\n")

    user_proxy.initiate_chat(
        react_agent,
        message=query
    )