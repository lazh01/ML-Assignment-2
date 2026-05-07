# AI-Powered Research Paper Discovery System

A multi-agent system for discovering and evaluating research papers based on user queries with structured constraints.

## Project Overview

This project implements an intelligent research paper discovery system that helps users find relevant academic papers by parsing natural language queries into structured constraints and leveraging multiple data sources.

### Architecture Approach: Pipeline-Based Agent System

The project explored three different approaches to multi-agent orchestration:

1. **Pipeline-Based (Chosen)** - Used in the base implementation
   - Deterministic, structured workflow: Parse → Search → Filter → Rank
   - Uses LLM to extract constraints from natural language queries
   - Processes results through deterministic filters
   - LLM ranks candidates and provides explanations
   - **Advantages**: Stable, predictable, fewer API rate limit issues, faster iteration
   - **Disadvantages**: Less flexible for complex queries requiring multiple reasoning steps

2. **GroupChat-Based** (Option 2)
   - Multiple agents collaborate through conversation
   - Agents can have complex back-and-forth discussions
   - **Advantages**: Great versatility for complex scenarios
   - **Disadvantages**: Risk of infinite loops, hallucination, expensive token usage, semantic scholar rate limiting

3. **ReAct-Based** (Option 3)
   - Agent reasons through steps and takes actions iteratively
   - **Advantages**: Good for dynamic problem-solving
   - **Disadvantages**: Similar looping and rate-limiting issues as GroupChat

**Why Pipeline Was Selected**: While GroupChat and ReAct offer greater versatility, their iterative nature caused excessive API calls to Semantic Scholar and frequent rate limiting during testing. The pipeline approach provided a better balance of functionality and stability for production use, with deterministic behavior and fewer failure modes.

## Data Sources

- **OpenAlex API** - Primary source for paper metadata (no API key required)
- **Semantic Scholar** - Alternative data source for citation verification (Optional, configured in code)

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Internet connection (for API calls)

### Step 1: Clone/Download the Project

```bash
cd path/to/ML-Assignment-2
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Dependencies

- **autogen-agentchat** - Multi-agent orchestration framework
- **autogen** - Core AutoGen library (v0.3.1)
- **mistralai** - Mistral AI API client (v1.2.3)
- **ollama** - Local model support (v0.3.3)
- **fix-busted-json** - JSON repair utility for handling malformed responses

## Configuration

### API Key Setup

The system uses the Mistral AI API for LLM capabilities. Configure your API key as follows:

#### Option 1: Direct Configuration (In Code)

Edit `config/llm_config.py`:

```python
config_list = [
    {
        "model": "open-mistral-nemo",
        "api_key": "YOUR_API_KEY_HERE",  # Replace with your Mistral API key
        "api_type": "mistral",
        "api_rate_limit": 0.25,
        "repeat_penalty": 1.1,
        "temperature": 0.0,
        "seed": 42,
        "stream": False,
        "native_tool_calls": False,
        "cache_seed": None,
        "verbose": True,
    }
]
```

#### Option 2: Environment Variable (Recommended for Production)

Set an environment variable:

```bash
# Windows (PowerShell)
$env:MISTRAL_API_KEY = "your_api_key_here"

# Windows (Command Prompt)
set MISTRAL_API_KEY=your_api_key_here

# macOS/Linux
export MISTRAL_API_KEY="your_api_key_here"
```

Then update `config/llm_config.py`:

```python
api_key = os.getenv("MISTRAL_API_KEY")
```

### Obtaining API Keys

1. **Mistral API Key**:
   - Visit: https://console.mistral.ai/
   - Sign up for an account
   - Navigate to API Keys section
   - Generate a new API key
   - Copy and paste into configuration

## Running the Agent

### Basic Usage

Run the interactive research agent:

```bash
python main.py
```

You will be prompted to enter a research query:

```
Enter your research query: Find a research paper about large language models published after 2022 with at least 100 citations. Explain why it is relevant.
```

The system will:
1. **Parse** the query into structured constraints (topic, year range, citation threshold)
2. **Search** OpenAlex for papers matching the topic
3. **Filter** results based on extracted constraints
4. **Rank** and select the best match with explanations
5. **Return** detailed information about the selected paper

### Output Format

The system returns:
- Title, authors, year
- Citation count and source
- Link to paper
- LLM-generated explanation and reasoning

## Evaluation Reflection

The system was evaluated against 12 diverse test prompts covering broad topics, narrow topics, exact constraints, ambiguous queries, and impossible scenarios.

### Test Coverage(See evaluation_results.json for verbose results)

| Prompt | Topic | Constraints | Result | Match Quality |
|--------|-------|-------------|--------|---|
| 1 | Transformer models | after 2017 | DNABERT (2021, 1169 cit.) | ✓ Good |
| 2 | RAG for QA | before 2021, ≥100 cit. | Seq2Seq Summarization (2016, 2201 cit.) | ~ Tangential |
| 3 | Reinforcement learning | 2017, ≥200 cit. | Deep RL Robotics (2017, 1444 cit.) | ✓ Perfect |
| 4 | AI agents with tools | after 2022 | CottonBot (2025, 2 cit.) | ~ Loosely related |
| 5 | Graph neural networks | before 2020, ≥100 cit. | GNN Review (2018, 1451 cit.) | ✓ Good |
| 6 | Diffusion models | >1000 cit. | Latent Diffusion (2022, 13230 cit.) | ✓ Excellent |
| 7 | AI safety | (no constraints) | AI Safety Gridworlds (2017, 117 cit.) | ✓ Good |
| 8 | Broccoli compiler optimization | after 2023, ≥50 cit. | Microgreens (2024, 50 cit.) | ✗ Wrong topic |
| 9 | Autonomous software agents | after 2021, >50 cit. | LLMs for Software Eng. (2025, 55 cit.) | ~ Barely meets citations |
| 10 | Retrieval systems for LLMs | ≥200 cit. | Vector Space Models (2010, 2866 cit.) | ~ Loosely related |
| 11 | Multimodal AI (influential) | (no constraints) | Multimodal Biomedical AI (2022, 1053 cit.) | ✓ Good |
| 12 | Quantum machine learning | after 2020, >200 cit. | Power of Data in QML (2021, 621 cit.) | ✓ Good |

### What works well

- **Exact year constraints**: Queries that specify a publication year or year range generally produce correct matches.
- **High citation retrieval**: Very high citation queries are handled well when the candidate set includes strong, well-known papers.
- **Broad topic retrieval**: General prompts like "transformer models" and "AI safety" return relevant papers.
- **Ranking stage**: The research agent formats responses cleanly and explains why the selected paper was chosen.

### What fails or is unreliable

- **Topic enforcement**: The broccoli query highlights a weakness: if OpenAlex returns a candidate list containing a paper that it believes is related, the pipeline cannot reject it on topic alone unless the topic is explicitly checked in the filter. The system should instead have the research agent say "No papers found" if none of the candidates are truly relevant.
- **Limited candidate set**: OpenAlex returns a fixed set of papers per query, and the system only ranks that list. It is unclear whether OpenAlex chooses the candidates by relevance, recency, citation count, or a combination. Because the candidate set is limited, the research agent can only choose the best paper from that subset, not from the full literature.
- **Loose relevance**: Some results are related but not a tight match to the query, especially for queries that require a specific technical focus.

### Constraint adherence

- **Year constraints**: Generally enforced.
- **Citation constraints**: The system uses OpenAlex filtering and local validation, but the final ranking stage may still choose a lower-cited paper from the retrieved candidates if it is deemed more relevant.
- **Topic constraints**: The weakest link. The data stage can only filter what OpenAlex provides; if OpenAlex believes a paper fits the topic, the pipeline must rely on stricter downstream checks.

### OpenAlex behavior note

OpenAlex returns a candidate list ordered by its internal relevance scoring for the query. The research agent must choose from the papers OpenAlex considers most relevant to the request.

### LLM behavior note

- The research agent selects the most relevant paper from the retrieved list. Depending on how it evaluates relevance, it may prefer a less-cited paper if it feels that paper fits the query better.
- This means low citation counts are not necessarily wrong if the paper is still the best candidate from the limited OpenAlex results.

### Next steps to improve robustness

1. **Strict topic filtering**: Add deterministic topic checks that reject papers unless the topic appears clearly in the title or abstract.
2. **Agent no-result policy**: Configure the research agent to return "No papers found" when the candidate list does not contain a truly relevant match, even if other constraints are met.
3. **Candidate validation**: Validate results against metadata before ranking, rather than relying only on the research agent’s assessment.
4. **Understand OpenAlex selection**: Investigate how OpenAlex chooses its candidate list and consider retrieving more papers if the first page is too narrow.


## Reflection

### Approach Comparison: Pipeline vs. GroupChat vs. ReAct

The project explored three distinct agent orchestration strategies, each with different trade-offs.

#### What worked well?

- **Pipeline**: Deterministic, predictable control flow. The LLM is invoked at specific stages (constraint extraction, then ranking). Results are stable and repeatable. The search tool is fully implemented with robust logic to convert natural language constraints into API queries.
- **Constraint extraction**: Even with an LLM-based planner, forcing structured JSON output and normalizing year/citation ranges into canonical fields works reliably.
- **OpenAlex integration**: Once filter syntax was corrected (using `>` instead of `>=`), the API integration was straightforward and performant.

#### What failed or was unreliable?

- **GroupChat and ReAct**: Both approaches gave agents tool access and autonomy to decide when and how to call tools. Behavior was erratic:
  - Sometimes the agent skipped the tool entirely and hallucinated results.
  - Other times the agent entered loops, repeatedly calling the same tool with slight variations and never reaching a conclusion.
  - Semantic Scholar API rate limits were hit frequently due to excessive tool invocations.
- **Agent coordination**: When multiple agents or a single agent with multiple reasoning steps were involved, they often failed to ground their reasoning in actual tool outputs.

#### How often did the agent need tool calls?

- **Pipeline**: Exactly 2 LLM calls per query (planner + research agent). The search tool is always called once, deterministically.
- **GroupChat/ReAct**: Highly variable and unpredictable. Some queries completed with 1-2 tool calls; others triggered 10+ calls before hitting rate limits or timing out.

#### Did the LLM ever hallucinate?

Yes, frequently:
- **GroupChat/ReAct**: The agents hallucinated paper titles, authors, and citation counts when they skipped tool calls. They also fabricated explanations without consulting actual search results.
- **Pipeline (ranking stage)**: The research agent sometimes selected papers that loosely matched the query and provided post-hoc justifications that didn't align with the actual constraints. For example, a paper with low citations was selected for a query with a high citation threshold, then justified as acceptable because it was "foundational."

#### How did you prevent incorrect answers?

- **Constraint enforcement**: The pipeline uses deterministic filtering—year ranges, citation thresholds, and topic keywords are checked before the LLM ranks candidates. If no papers pass all constraints, the system returns "No papers found" instead of allowing the LLM to invent one.
- **Tool correctness**: The search tool delegates filtering to OpenAlex's API (for year and citation counts) and to local deterministic logic (for topic matching). The LLM is only involved in ranking and explaining, not in constraint validation.
- **Reproducibility**: By controlling the order of operations (extract constraints → search → filter → rank), results are reproducible and auditable.

#### What would you improve with more time?

1. **Agent as tool user**: The assignment requires "an agent." A better approach would be to wrap the pipeline itself as a tool that an intelligent agent can invoke. The agent could handle more complex scenarios (multi-step queries, clarification of ambiguous constraints) without losing the reliability of the deterministic pipeline.

2. **Better LLM configuration**: The current approach uses a lighter model (Mistral Nemo). Larger, more instruction-tuned models might reduce hallucination in the ranking stage and allow safer tool autonomy in GroupChat/ReAct scenarios.

3. **Tool schema and validation**: If agents must have tool access, use strict tool schemas (e.g., function signatures with type hints) and validate all tool inputs and outputs before passing them to the next agent. This could prevent loops and hallucination.

4. **Code-executing agent**: Instead of giving the agent abstract tool access, a code-execution environment (e.g., Python with sandboxing) could allow the agent to write queries to the OpenAlex API or construct filters without pre-defined tool boundaries. This gives flexibility while maintaining determinism.

5. **Human-in-the-loop**: For truly ambiguous queries, the system could ask for clarification rather than guessing. For borderline results, ask the user to confirm constraints before finalizing a selection.

#### Summary

The pipeline approach prioritizes robustness and predictability over flexibility. GroupChat and ReAct prioritize autonomy but sacrifice reliability. For a production system, the pipeline is safer. For research and exploration, a more capable model with tighter tool schema and intermediate validation could make agent autonomy more viable.

