"""Quickstart demo using a research agent with web search."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from deepagents import create_deep_agent
from dotenv import load_dotenv

from config import get_model
from prompts import load_prompt
from tools.search import tavily_search
from tools.thinking import think_tool

load_dotenv()

agent = create_deep_agent(
    tools=[tavily_search, think_tool],
    system_prompt=load_prompt("research"),
    model=get_model("openai:gpt-4o"),
)

if __name__ == "__main__":
    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": "你是哪个模型？你的版本号是什么？",
        }]
    })
    print(result["messages"][-1].content)
