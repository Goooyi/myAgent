# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

myAgent is a Python agent project using the DeepAgents framework (built on LangChain/LangGraph). The project explores building agents compatible with Harbor Framework and Inspect AI for evaluation/benchmarking.

## Development Commands

```bash
# Install dependencies (uses uv package manager)
uv sync

# Run demos
python demo/quickstart.py          # Agent with web search tool
python demo/model_customization.py # Custom model configuration

# Run main entry point
python main.py
```

## Architecture

**Core Pattern:** DeepAgents wraps LangChain to create agents with tools and system prompts.

```python
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model

# Create agent with tools
agent = create_deep_agent(
    tools=[my_tool_function],
    system_prompt="Your instructions here",
    model=init_chat_model("openai:gpt-4o"),  # optional custom model
)

# Invoke agent
result = agent.invoke({"messages": [{"role": "user", "content": "..."}]})
```

**Key Dependencies:**
- `deepagents` - Agent creation framework
- `langchain-openai` - LLM integration
- `tavily-python` - Web search tool

## Environment Configuration

Required environment variables in `.env`:
- `OPENAI_API_KEY` - OpenAI API key (or compatible endpoint key)
- `OPENAI_API_BASE` - Custom API endpoint (optional)
- `TAVILY_API_KEY` - For web search functionality

## Project Goal

Build agents compatible with:
- [Harbor Framework](https://harborframework.com/docs/agents#integrating-your-own-agent)
- [Inspect AI](https://inspect.aisi.org.uk/agent-custom.html)
