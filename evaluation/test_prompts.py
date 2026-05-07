EVALUATION_PROMPTS = [

    # Broad topic
    "Find a highly cited paper about transformer models published after 2018.",

    # Narrow topic
    "Find a paper about retrieval-augmented generation for question answering published before 2021 with at least 500 citations.",

    # Exact year
    "Find a paper about reinforcement learning published in exactly 2017 with at least 1000 citations.",

    # After year
    "Find a recent paper about AI agents using tools published after 2023.",

    # Before year
    "Find a paper about graph neural networks published before 2019 with at least 300 citations.",

    # High citation constraint
    "Find a paper about diffusion models with more than 2000 citations.",

    # Ambiguous request
    "Find a good paper about AI safety.",

    # Likely no-result case
    "Find a paper about using broccoli to optimize compiler design published after 2024 with at least 100 citations.",

    # Very narrow constraint combination
    "Find a paper about autonomous software engineering agents published after 2022 with more than 100 citations.",

    # Another realistic industry case
    "Find a paper about retrieval systems for LLMs with at least 400 citations and explain why it would matter for enterprise search systems.",

    # Ambiguous + vague citations
    "Find an influential paper about multimodal AI.",

    # Extremely difficult constraint
    "Find a paper about quantum machine learning published in 2025 with more than 5000 citations."
]