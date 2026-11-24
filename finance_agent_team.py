"""Multi-agent financial assistant adapted from awesome-llm-apps for OpenRouter.

This is an educational demo, not investment advice. Market data may be delayed,
incomplete, or unavailable. Never treat generated analysis as a trading signal.
"""
from __future__ import annotations

import os
from dotenv import load_dotenv

from agno.agent import Agent
from agno.team import Team
from agno.models.openrouter import OpenRouter
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

load_dotenv()

MODEL_ID = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
DB_PATH = os.getenv("AGENT_DB_PATH", "data/agents.db")

def build_team() -> Team:
    """Build a web + finance agent team using OpenRouter for all LLM calls."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is missing. Copy .env.example to .env "
            "and add a newly generated OpenRouter key."
        )

    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    db = SqliteDb(db_file=DB_PATH)

    def model() -> OpenRouter:
        return OpenRouter(id=MODEL_ID, api_key=api_key, max_tokens=2048)

    web_agent = Agent(
        name="Web Research Agent",
        role="Find recent, relevant public information and cite source URLs.",
        model=model(),
        tools=[DuckDuckGoTools()],
        db=db,
        add_history_to_context=True,
        markdown=True,
        instructions=[
            "Search the web when the question requires current information.",
            "Separate verified facts from interpretation.",
            "Include source URLs for important claims.",
            "If sources disagree or evidence is missing, say so clearly.",
        ],
    )

    finance_agent = Agent(
        name="Financial Data Agent",
        role="Retrieve and explain company and market data.",
        model=model(),
        tools=[
            YFinanceTools(
                enable_stock_price=True,
                enable_analyst_recommendations=True,
                enable_company_info=True,
                enable_company_news=True,
            )
        ],
        db=db,
        add_history_to_context=True,
        markdown=True,
        instructions=[
            "Use the available finance tools for ticker-specific market data.",
            "Never invent prices, ratios, analyst recommendations, or news.",
            "Always state the ticker and the time sensitivity of market data.",
            "Use tables for numerical comparisons.",
            "Do not give personalized investment advice or tell users to buy or sell.",
        ],
    )

    return Team(
        name="OpenRouter Finance Agent Team",
        model=model(),
        members=[web_agent, finance_agent],
        db=db,
        markdown=True,
        debug_mode=False,
        instructions=[
            "Coordinate the web and finance agents when both current context and "
            "financial data are useful.",
            "Synthesize the agents' findings into one concise answer.",
            "Clearly label data, assumptions, uncertainty, and source links.",
            "This is an educational analysis tool, not a financial adviser.",
        ],
    )


if __name__ == "__main__":
    team = build_team()
    print("Finance Agent Team ready. Type 'exit' to quit.")
    while True:
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        if question.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break
        if question:
            team.print_response(question, stream=True)
