from unittest.mock import MagicMock

from src.feedback_analyzer import analyze_feedback


def build_fake_client(model_response: str) -> MagicMock:
    client = MagicMock()
    client.chat.completions.create.return_value.choices[0].message.content = model_response
    return client


def test_analyze_feedback_returns_model_categories_and_counts():
    client = build_fake_client(
        """
        {
          "items": [
            {
              "feedback": "页面报错无法提交",
              "category": "bug",
              "priority": "P0",
              "reason": "核心提交流程不可用。"
            }
          ]
        }
        """
    )

    result = analyze_feedback("页面报错无法提交", client)

    assert result["total_count"] == 1
    assert result["category_counts"] == {
        "bug": 1,
        "experience": 0,
        "feature_request": 0,
        "other": 0,
    }
    assert result["priorities"][0] == {
        "priority": "P0",
        "feedback": "页面报错无法提交",
        "category": "bug",
        "reason": "核心提交流程不可用。",
    }
    assert client.chat.completions.create.call_count == 1
