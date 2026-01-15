from deepagents import create_deep_agent
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model("openai:gpt-4o")
agent = create_deep_agent(
    model=model,
)
