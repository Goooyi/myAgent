"""PM Agent factory.

Creates a configured PM agent with tools and sub-agents.
"""

from deepagents import create_deep_agent

from agents.pm_agent.prompts import get_pm_instructions, get_research_instructions
from config import get_model
from tools.prd import parse_mermaid_to_prd, parse_prd_to_mermaid, validate_prd
from tools.search import tavily_search
from tools.thinking import think_tool


def create_pm_agent(
    model_name: str = "anthropic:claude-sonnet-4-20250514",
    **model_kwargs,
):
    """Create a PM agent with all tools and sub-agents configured.

    Args:
        model_name: LLM model identifier (default: Claude Sonnet 4)
        **model_kwargs: Additional arguments passed to init_chat_model

    Returns:
        Configured deepagent ready to invoke
    """
    model = get_model(model_name, **model_kwargs)

    research_subagent = {
        "name": "research-agent",
        "description": "Delegate market research, competitor analysis, or trend research to this sub-agent.",
        "system_prompt": get_research_instructions(),
        "tools": [tavily_search, think_tool],
    }

    agent = create_deep_agent(
        model=model,
        tools=[
            parse_prd_to_mermaid,
            parse_mermaid_to_prd,
            validate_prd,
            tavily_search,
            think_tool,
        ],
        system_prompt=get_pm_instructions(),
        subagents=[research_subagent],
    )

    return agent
