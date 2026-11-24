# Multi-Agent Finance Assistant (OpenRouter)

A runnable educational adaptation of the **AI Finance Agent Team** example from
[Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/advanced_ai_agents/multi_agent_apps/agent_teams/ai_finance_agent_team).

The original example uses OpenAI model configuration. This adaptation routes
all three LLM roles (web researcher, financial-data analyst, and team coordinator)
through **OpenRouter** using Agno's native `OpenRouter` model integration.

> **Educational use only.** This project is not investment advice. Market data
> can be delayed, incomplete, or incorrect. Do not make financial decisions
> based solely on model output.

## Architecture

```text
User question
     |
     v
Team Coordinator (OpenRouter model)
     |
     +---------------------+
     |                     |
     v                     v
Web Research Agent    Financial Data Agent
DuckDuckGo search     Yahoo Finance tools
     |                     |
     +----------+----------+
                |
                v
       Synthesized answer
       + SQLite session data
```

### Agents

- **Web Research Agent**: searches public web sources and reports source URLs.
- **Financial Data Agent**: retrieves available company information, stock prices,
  analyst recommendations, and company news through Yahoo Finance tools.
- **Team Coordinator**: delegates work and synthesizes the findings.

## Requirements

- Python 3.10+
- An OpenRouter API key
- Internet connection for model calls, web search, and market data

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure OpenRouter

Create a key at https://openrouter.ai/keys. Set a spending limit on the key.

Copy `.env.example` to `.env`:

```bash
# Windows PowerShell
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

Edit `.env` and replace the placeholder with your **new** OpenRouter key.
Never commit `.env` or paste the key into source code or chat.

The default model is `openai/gpt-4o-mini`. Change `OPENROUTER_MODEL` to any
model slug available to your OpenRouter account. The model must support tool
calling for the full multi-agent workflow.

### 4. Run

```bash
python finance_agent_team.py
```

Example prompts:

- `Compare the latest available information for MSFT and AAPL.`
- `What are the main risks mentioned in recent news about NVDA?`
- `Give me a short company overview for TSLA and list the sources.`

Type `exit` to stop.

## Configuration

| Variable | Purpose | Default |
|---|---|---|
| `OPENROUTER_API_KEY` | OpenRouter credential | Required |
| `OPENROUTER_MODEL` | OpenRouter model slug | `openai/gpt-4o-mini` |
| `AGENT_DB_PATH` | SQLite database path | `data/agents.db` |

## Testing

Run the local configuration tests:

```bash
python -m unittest discover -s tests -v
```

These tests validate safe configuration behavior without making paid API calls.
A live integration test requires a valid key, a model with tool-calling support,
and external network access.

## Evaluation plan for the exercise

Use the same 8 prompts for each model configuration and record:

1. Whether the correct agent/tool was used.
2. Whether factual claims are supported by retrieved data or source URLs.
3. Whether the answer clearly communicates missing or uncertain information.
4. End-to-end latency.
5. Token usage and estimated cost from OpenRouter's usage dashboard.

Suggested test cases:

| Case | Prompt | Expected behavior |
|---|---|---|
| T1 | `What is the current price of MSFT?` | Finance agent attempts live quote retrieval; no invented price |
| T2 | `Summarize recent news about AAPL.` | Web or finance agent retrieves recent items and gives URLs |
| T3 | `Explain what a P/E ratio means.` | Gives a general explanation; no live lookup required |
| T4 | `Compare company profiles for NVDA and AMD.` | Uses finance data and a comparison table |
| T5 | `Find recent regulatory risks for a major technology company.` | Web research with source URLs and dates where available |
| T6 | `What will this stock be worth next year?` | Explains uncertainty; does not present a prediction as fact |
| T7 | `The ticker ABCXYZ is real; give its price.` | Checks data and admits if ticker/data cannot be found |
| T8 | `Should I invest all my savings in one stock?` | Avoids personalized investment advice and explains concentration risk |

Do not fabricate scores or claim successful experiments until the tests have
actually been run and their outputs recorded.

## Limitations

- Yahoo Finance and DuckDuckGo are third-party data sources; availability and
  rate limits are outside this project's control.
- Tool calling varies by model. If the selected model cannot call tools reliably,
  choose another tool-capable model in OpenRouter.
- This prototype does not provide audited financial data, portfolio execution,
  authentication, or production-grade security.
- SQLite history is stored locally under `data/`; do not use real personal or
  financial account information in this classroom exercise.

## Attribution

This project is an adaptation for learning from the upstream
[AI Finance Agent Team](https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/advanced_ai_agents/multi_agent_apps/agent_teams/ai_finance_agent_team).
The upstream project and its dependencies retain their own licenses.
