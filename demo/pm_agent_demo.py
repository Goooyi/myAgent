"""Demo for the PM (Product Manager) agent."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

from agents import create_pm_agent

load_dotenv()

if __name__ == "__main__":
    agent = create_pm_agent()

    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": "我想做一个帮助用户学英语的 AI 应用",
        }]
    })

    print(result["messages"][-1].content)
