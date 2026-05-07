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

