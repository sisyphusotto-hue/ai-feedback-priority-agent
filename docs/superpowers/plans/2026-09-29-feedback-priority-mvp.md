# AI User Feedback Priority Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (or subagent-driven-development when available) to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a small, demonstrable web tool that turns pasted user feedback into issue categories, counts, and P0/P1/P2 product priorities.

**Architecture:** The first version uses a pure Python analyzer so the core priority rules are testable without an API key. Streamlit provides one text input and a clearly separated result area. A later iteration can replace only the classification layer with an LLM API while preserving the result schema.

**Tech Stack:** Python 3.13, Streamlit, pytest.

## Global Constraints

- Create a separate project at `ai-feedback-priority-agent`; do not modify `ai-resume-job-match-agent`.
- Use public simulated feedback only; do not request real customer data.
- Do not add or commit API keys.
- The MVP accepts one feedback item per line and ignores blank lines.
- Categories are `bug`, `experience`, `feature_request`, and `other`.
- Priority rules are deterministic: any bug containing “无法”, “失败”, “报错”, or “闪退” is P0; categories with two or more items are P1; all other items are P2.

---

### Task 1: Testable feedback analysis core

**Files:**
- Create: `src/feedback_analyzer.py`
- Create: `tests/test_feedback_analyzer.py`

**Interfaces:**
- Consumes: `feedback_text: str`
- Produces: `analyze_feedback(feedback_text: str) -> dict` with `total_count`, `category_counts`, and `priorities`.

- [ ] **Step 1: Write the failing test**

```python
from src.feedback_analyzer import analyze_feedback


def test_analyze_feedback_counts_categories_and_priorities():
    result = analyze_feedback("页面报错无法提交\n希望增加深色模式\n页面加载太慢")

    assert result["total_count"] == 3
    assert result["category_counts"] == {
        "bug": 1,
        "experience": 1,
        "feature_request": 1,
        "other": 0,
    }
    assert result["priorities"][0]["priority"] == "P0"
    assert result["priorities"][0]["feedback"] == "页面报错无法提交"
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `py -m pytest tests/test_feedback_analyzer.py -v`

Expected: `ModuleNotFoundError: No module named 'src.feedback_analyzer'`.

- [ ] **Step 3: Write the minimal implementation**

Create `analyze_feedback` and small helper functions that split lines, classify each line, count categories, and assign P0/P1/P2 using the global rules.

- [ ] **Step 4: Run the test to verify it passes**

Run: `py -m pytest tests/test_feedback_analyzer.py -v`

Expected: `1 passed`.

### Task 2: Streamlit demonstration page

**Files:**
- Create: `app.py`
- Create: `tests/test_app.py`
- Create: `requirements.txt`

**Interfaces:**
- Consumes: multiline feedback from `st.text_area`.
- Produces: total feedback count, category statistics, and a priority list in the browser.

- [ ] **Step 1: Write the failing UI test**

```python
from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_app_analyzes_feedback_after_button_click():
    app = AppTest.from_file(Path(__file__).parents[1] / "app.py")
    app.run()

    app.text_area[0].input("页面报错无法提交\n希望增加深色模式")
    app.button[0].click().run()

    assert app.metric[0].value == "2"
    assert "优先级建议" in [header.value for header in app.subheader]
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `py -m pytest tests/test_app.py -v`

Expected: failure because `app.py` does not yet exist.

- [ ] **Step 3: Write the minimal Streamlit page**

Create a page titled `AI 用户反馈分析与需求优先级 Agent`, add a text area with one feedback item per line, a `开始分析` button, and result sections for total count, category counts, and `优先级建议`.

- [ ] **Step 4: Run all tests**

Run: `py -m pytest -v`

Expected: all tests pass.

### Task 3: Sample data, README, and local demo evidence

**Files:**
- Create: `data/sample_feedback.txt`
- Create: `README.md`
- Create: `.gitignore`

**Interfaces:**
- Consumes: simulated feedback in `data/sample_feedback.txt`.
- Produces: reproducible local start instructions and an explanation of the P0/P1/P2 rules.

- [ ] **Step 1: Add six simulated feedback lines**

Include one P0 submission failure, two feature requests, two experience issues, and one other item. Do not include personal information.

- [ ] **Step 2: Write README startup instructions**

Include these commands:

```powershell
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

- [ ] **Step 3: Verify the full test suite and record the result**

Run: `py -m pytest -v`

Expected: no failures.

### Plan self-review

- Scope covers one independent, testable MVP: feedback input, categorization, priority output, local web page, sample data, and documentation.
- No real customer data, API key, login, CSV parser, database, or deployment is included in this first version.
- All production behavior has a test-first task.
