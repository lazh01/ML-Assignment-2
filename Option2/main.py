from Option2.workflow.pipeline import manager, user_proxy

if __name__ == "__main__":

    query = input("Enter your research query: ")

    user_proxy.initiate_chat(
        manager,
        message=query,
    )