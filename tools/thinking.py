"""Thinking tool for strategic reflection during agent execution."""

from langchain_core.tools import tool


@tool(parse_docstring=True)
def think_tool(reflection: str) -> str:
    """Tool for strategic reflection on progress and decision-making.

    Use this tool to pause and assess progress, analyze findings, identify gaps,
    and plan next steps systematically.

    Args:
        reflection: Your detailed reflection on progress, findings, gaps, and next steps

    Returns:
        Confirmation that reflection was recorded
    """
    return f"Reflection recorded: {reflection}"
