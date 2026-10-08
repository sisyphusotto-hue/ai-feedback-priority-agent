import json
from collections import Counter


CATEGORIES = ("bug", "experience", "feature_request", "other")
PRIORITIES = ("P0", "P1", "P2")


def analyze_feedback(feedback_text: str, client: object) -> dict:
    feedback_items = [line.strip() for line in feedback_text.splitlines() if line.strip()]
    if not feedback_items:
        return empty_result()

    response = client.chat.completions.create(
        model="deepseek-chat",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "你是产品反馈分析助手，只输出符合要求的 JSON。",
            },
            {"role": "user", "content": build_analysis_prompt(feedback_items)},
        ],
    )
    raw_content = response.choices[0].message.content
    analyzed_items = parse_model_items(raw_content)
    category_counts = Counter(item["category"] for item in analyzed_items)

    return {
        "total_count": len(analyzed_items),
        "category_counts": {
            category: category_counts.get(category, 0) for category in CATEGORIES
        },
        "priorities": sorted(
            analyzed_items, key=lambda item: (item["priority"], item["feedback"])
        ),
    }


def build_analysis_prompt(feedback_items: list[str]) -> str:
    feedback_lines = "\n".join(
        f"{index}. {feedback}" for index, feedback in enumerate(feedback_items, start=1)
    )
    return f"""请逐条分析以下模拟用户反馈。

反馈：
{feedback_lines}

分类只能从 bug、experience、feature_request、other 中选择。
优先级只能从 P0、P1、P2 中选择：P0 表示核心流程不可用或严重故障；P1 表示明显影响体验或多用户问题；P2 表示单条需求或低风险问题。
必须仅返回以下 JSON，不要使用 Markdown 代码块：
{{
  "items": [
    {{
      "feedback": "原始反馈文本",
      "category": "bug",
      "priority": "P0",
      "reason": "不超过 30 字的判断原因"
    }}
  ]
}}
"""


def parse_model_items(raw_content: str | None) -> list[dict]:
    if not raw_content:
        raise ValueError("模型没有返回分析结果。")

    content = raw_content.strip()
    if content.startswith("```"):
        content = content.split("\n", maxsplit=1)[1].rsplit("```", maxsplit=1)[0].strip()

    data = json.loads(content)
    items = data.get("items")
    if not isinstance(items, list):
        raise ValueError("模型返回格式缺少 items 列表。")

    normalized_items = []
    for item in items:
        category = item.get("category")
        priority = item.get("priority")
        feedback = item.get("feedback")
        reason = item.get("reason")
        if category not in CATEGORIES or priority not in PRIORITIES:
            raise ValueError("模型返回了不支持的分类或优先级。")
        if not all(isinstance(value, str) and value.strip() for value in (feedback, reason)):
            raise ValueError("模型返回的反馈文本或原因为空。")
        normalized_items.append(
            {
                "feedback": feedback.strip(),
                "category": category,
                "priority": priority,
                "reason": reason.strip(),
            }
        )
    return normalized_items


def empty_result() -> dict:
    return {
        "total_count": 0,
        "category_counts": {category: 0 for category in CATEGORIES},
        "priorities": [],
    }
