import pytest

from src.deepseek_client import get_api_key


def test_get_api_key_prefers_streamlit_secret():
    assert get_api_key({"DEEPSEEK_API_KEY": "test-secret"}) == "test-secret"


def test_get_api_key_raises_when_missing(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    with pytest.raises(ValueError, match="DEEPSEEK_API_KEY"):
        get_api_key({})
