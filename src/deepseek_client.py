import os

from openai import OpenAI


def get_api_key(secrets: dict | None = None) -> str:
    api_key = (secrets or {}).get("DEEPSEEK_API_KEY") or os.getenv(
        "DEEPSEEK_API_KEY"
    )
    if not api_key:
        raise ValueError("没有读取到 DEEPSEEK_API_KEY，请在 Streamlit Secrets 中配置。")
    return api_key


def create_client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
