import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from deepagents import create_deep_agent
from dotenv import load_dotenv
from tavily import TavilyClient

from config import get_model
from prompts import load_prompt

load_dotenv()

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def internet_search(query: str, max_results: int = 5):
    """Run a web search"""
    return tavily_client.search(query, max_results=max_results)


agent = create_deep_agent(
    tools=[internet_search],
    system_prompt=load_prompt("research"),
    model=get_model("openai:gpt-4o"),
)

result = agent.invoke({"messages": [{"role": "user", "content": "你是哪个模型？你的版本号是什么？"}]})
print(result["messages"][-1].content)
