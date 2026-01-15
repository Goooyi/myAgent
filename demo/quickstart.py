import os

from deepagents import create_deep_agent
from dotenv import load_dotenv
from langchain_core.load import load
from tavily import TavilyClient

load_dotenv()

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def internet_search(query: str, max_results: int = 5):
    """Run a web search"""
    return tavily_client.search(query, max_results=max_results)


agent = create_deep_agent(
    tools=[internet_search],
    system_prompt="Conduct research and write a polished report.",
)

result = agent.invoke({"messages": [{"role": "user", "content": "你是谁"}]})
