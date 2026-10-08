from pathlib import Path

from streamlit.testing.v1 import AppTest

from src import deepseek_client, feedback_analyzer


SAMPLE_RESULT = {
    "total_count": 1,
    "category_counts": {
        "bug": 1,
        "experience": 0,
        "feature_request": 0,
        "other": 0,
    },
    "priorities": [
        {
            "feedback": "页面报错无法提交",
            "category": "bug",
            "priority": "P0",
            "reason": "核心提交流程不可用。",
        }
    ],
}


def test_app_renders_api_analysis_after_button_click(monkeypatch):
    monkeypatch.setattr(deepseek_client, "get_api_key", lambda secrets: "test-key")
    monkeypatch.setattr(deepseek_client, "create_client", lambda api_key: object())
    monkeypatch.setattr(
        feedback_analyzer, "analyze_feedback", lambda feedback_text, client: SAMPLE_RESULT
    )

    app = AppTest.from_file(Path(__file__).parents[1] / "app.py")
    app.run()

    app.text_area[0].input("页面报错无法提交")
    app.button[0].click().run()

    assert app.metric[0].value == "1"
    assert "优先级建议" in [header.value for header in app.subheader]
    assert "P0" in app.markdown[-1].value


def test_app_shows_friendly_error_when_api_key_is_missing(monkeypatch):
    monkeypatch.setattr(
        deepseek_client,
        "get_api_key",
        lambda secrets: (_ for _ in ()).throw(ValueError("没有读取到 DEEPSEEK_API_KEY")),
    )

    app = AppTest.from_file(Path(__file__).parents[1] / "app.py")
    app.run()

    app.text_area[0].input("页面报错无法提交")
    app.button[0].click().run()

    assert "DEEPSEEK_API_KEY" in app.error[0].value
