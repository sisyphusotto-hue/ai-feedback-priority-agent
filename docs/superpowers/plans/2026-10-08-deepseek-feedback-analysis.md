# DeepSeek Feedback Analysis Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the feedback-priority MVP so DeepSeek classifies each simulated feedback item and returns a structured priority recommendation.

**Architecture:** `src/feedback_analyzer.py` will build a feedback-specific JSON prompt, call an injected OpenAI-compatible client, parse the model response, and calculate counts from returned categories. `src/deepseek_client.py` will independently load `DEEPSEEK_API_KEY` and create a client. `app.py` will use this API workflow and show a friendly error when no deployment secret is configured.

**Tech Stack:** Python, Streamlit, OpenAI Python SDK, DeepSeek API, pytest

## Global Constraints

- This repository remains independent from the resume and customer-service projects.
- Use only simulated feedback entered by the user; do not require personal data.
- Read `DEEPSEEK_API_KEY` only from environment variables or Streamlit Secrets.
- Never commit a key, `.env`, or a Streamlit secrets file.
- Require model output as JSON with `items`; never parse free-form prose into categories.
- Use `deepseek-chat` through `https://api.deepseek.com`.

---

### Task 1: Add API-key and DeepSeek client helpers

**Files:**
- Create: `src/deepseek_client.py`
- Modify: `tests/test_deepseek_client.py`
- Modify: `requirements.txt`

**Interfaces:**
- Produces: `get_api_key(secrets: dict | None = None) -> str` and `create_client(api_key: str) -> OpenAI`.

- [ ] **Step 1: Write failing tests**

```python
from src.deepseek_client import get_api_key


def test_get_api_key_prefers_streamlit_secret():
    assert get_api_key({"DEEPSEEK_API_KEY": "test-secret"}) == "test-secret"


def test_get_api_key_raises_when_missing(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    with pytest.raises(ValueError, match="DEEPSEEK_API_KEY"):
        get_api_key({})
```

- [ ] **Step 2: Run the tests and confirm they fail because the module is absent**

Run: `py -m pytest tests/test_deepseek_client.py -v`

- [ ] **Step 3: Implement the helpers**

```python
def get_api_key(secrets: dict | None = None) -> str:
    api_key = (secrets or {}).get("DEEPSEEK_API_KEY") or os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("没有读取到 DEEPSEEK_API_KEY，请在 Streamlit Secrets 中配置。")
    return api_key


def create_client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
```

Add `openai` after `streamlit` in `requirements.txt`.

- [ ] **Step 4: Run tests and commit**

Run: `py -m pytest tests/test_deepseek_client.py -q`

```bash
git add requirements.txt src/deepseek_client.py tests/test_deepseek_client.py
git commit -m "feat: add DeepSeek client helper"
```

### Task 2: Replace rule classification with structured DeepSeek analysis

**Files:**
- Modify: `src/feedback_analyzer.py`
- Modify: `tests/test_feedback_analyzer.py`

**Interfaces:**
- Produces: `analyze_feedback(feedback_text: str, client: object) -> dict`.
- Model response: `{ "items": [{"feedback": str, "category": "bug|experience|feature_request|other", "priority": "P0|P1|P2", "reason": str}] }`.

- [ ] **Step 1: Write a failing fake-client test**

```python
def test_analyze_feedback_returns_model_categories_and_counts():
    client = build_fake_client(
        '{"items":[{"feedback":"页面报错无法提交","category":"bug","priority":"P0","reason":"核心提交流程不可用。"}]}'
    )
    result = analyze_feedback("页面报错无法提交", client)

    assert result["total_count"] == 1
    assert result["category_counts"]["bug"] == 1
    assert result["priorities"][0]["priority"] == "P0"
```

- [ ] **Step 2: Run the test and confirm it fails because the old function has no client parameter**

Run: `py -m pytest tests/test_feedback_analyzer.py::test_analyze_feedback_returns_model_categories_and_counts -v`

- [ ] **Step 3: Implement prompt, request, parsing, and count calculation**

Call `client.chat.completions.create` with model `deepseek-chat`, temperature `0.2`, and a prompt that restricts categories to `bug`, `experience`, `feature_request`, `other` and priorities to `P0`, `P1`, `P2`. Remove a Markdown JSON code fence before `json.loads`. Reject model responses with a missing `items` list.

- [ ] **Step 4: Run analyzer tests and commit**

Run: `py -m pytest tests/test_feedback_analyzer.py -q`

```bash
git add src/feedback_analyzer.py tests/test_feedback_analyzer.py
git commit -m "feat: analyze feedback with DeepSeek"
```

### Task 3: Use the API workflow in the Streamlit page and document secrets

**Files:**
- Modify: `app.py`
- Modify: `tests/test_app.py`
- Modify: `README.md`

**Interfaces:**
- Consumes: `get_api_key`, `create_client`, `analyze_feedback`.
- Produces: same visual result sections plus a friendly `st.error` if the API key is absent or the model returns invalid data.

- [ ] **Step 1: Write a failing app test that patches the API helpers**

```python
def test_app_passes_user_feedback_to_api_analyzer(monkeypatch):
    monkeypatch.setattr("src.deepseek_client.get_api_key", lambda secrets: "test-key")
    monkeypatch.setattr("src.deepseek_client.create_client", lambda api_key: object())
    monkeypatch.setattr("src.feedback_analyzer.analyze_feedback", lambda text, client: SAMPLE_RESULT)
```

The assertion must confirm the result section renders from `SAMPLE_RESULT` after clicking `开始分析`.

- [ ] **Step 2: Run the test and confirm it fails before the page passes a client**

Run: `py -m pytest tests/test_app.py -v`

- [ ] **Step 3: Implement Streamlit secret reading and error display**

Use `dict(st.secrets)` inside a helper that returns `{}` when secrets are absent. On button click: read key, create client, call `analyze_feedback(feedback_text, client)`, then render the existing result sections. Catch `ValueError`, `json.JSONDecodeError`, and API errors as one user-facing error message without printing the key.

- [ ] **Step 4: Document the public deployment setting**

README must state this version uses DeepSeek API and show only this safe Streamlit Secrets shape:

```toml
DEEPSEEK_API_KEY = "your-key-here"
```

- [ ] **Step 5: Run full verification and push**

Run: `py -m pytest -q` and `git diff --check`

```bash
git add app.py README.md tests/test_app.py
git commit -m "feat: connect Streamlit page to DeepSeek"
git push
```
