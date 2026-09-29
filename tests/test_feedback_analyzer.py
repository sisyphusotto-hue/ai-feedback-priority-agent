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
    assert result["priorities"][0] == {
        "priority": "P0",
        "feedback": "页面报错无法提交",
        "category": "bug",
        "reason": "影响核心流程，建议优先处理。",
    }
