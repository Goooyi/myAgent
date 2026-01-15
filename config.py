import os

import httpx
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()


def get_http_client() -> httpx.Client | None:
    """Get HTTP client with proxy if configured."""
    proxy = os.environ.get("HTTP_PROXY") or os.environ.get("HTTPS_PROXY")
    if proxy:
        return httpx.Client(proxy=proxy)
    return None


def get_async_http_client() -> httpx.AsyncClient | None:
    """Get async HTTP client with proxy if configured."""
    proxy = os.environ.get("HTTP_PROXY") or os.environ.get("HTTPS_PROXY")
    if proxy:
        return httpx.AsyncClient(proxy=proxy)
    return None


def get_model(model_name: str = "openai:gpt-4o", **kwargs):
    """Get a configured chat model with proxy support."""
    return init_chat_model(
        model_name,
        api_key=os.environ.get("OPENAI_API_KEY"),
        openai_api_base=os.environ.get("OPENAI_API_BASE"),
        http_client=get_http_client(),
        http_async_client=get_async_http_client(),
        **kwargs,
    )
