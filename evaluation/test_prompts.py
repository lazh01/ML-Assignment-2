EVALUATION_PROMPTS = [

    # Broad topic (easy retrieval baseline)
    "Find a highly cited paper about transformer models published after 2017.",

    # Narrow topic (still realistic)
    "Find a paper about retrieval-augmented generation for question answering published before 2021 with at least 100 citations.",

    # Exact year (realistic constraint)
    "Find a paper about reinforcement learning published in 2017 with at least 200 citations.",

    # After year (realistic modern area)
    "Find a recent paper about AI agents using tools published after 2022.",

    # Before year (well-established field)
    "Find a paper about graph neural networks published before 2020 with at least 100 citations.",

    # High citation constraint (realistic threshold)
    "Find a paper about diffusion models with more than 1000 citations.",

    # Ambiguous request (tests interpretation)
    "Find a good paper about AI safety.",

    # No-result case (INTENTIONALLY impossible, but not absurdly obscure)
    "Find a paper about using broccoli for compiler optimization published after 2023 with at least 50 citations.",

    # Multi-constraint but still realistic
    "Find a paper about autonomous software engineering agents published after 2021 with more than 50 citations.",

    # Realistic applied systems case
    "Find a paper about retrieval systems for large language models with at least 200 citations and explain why it matters for enterprise search systems.",

    # Ambiguous + no citation clarity
    "Find an influential paper about multimodal AI.",

    # Hard but still plausible (NOT impossible like 5000 citations in 2025)
    "Find a paper about quantum machine learning published after 2020 with more than 200 citations."
]