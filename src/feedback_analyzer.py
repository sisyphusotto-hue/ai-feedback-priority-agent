from collections import Counter


CATEGORIES = ("bug", "experience", "feature_request", "other")


def analyze_feedback(feedback_text: str) -> dict:
    feedback_items = [line.strip() for line in feedback_text.splitlines() if line.strip()]
    categorized_items = [
        {"feedback": item, "category": classify_feedback(item)}
        for item in feedback_items
    ]
    category_counts = Counter(item["category"] for item in categorized_items)

    return {
        "total_count": len(categorized_items),
        "category_counts": {
            category: category_counts.get(category, 0) for category in CATEGORIES
        },
        "priorities": build_priorities(categorized_items, category_counts),
    }


def classify_feedback(feedback: str) -> str:
    if any(keyword in feedback for keyword in ("无法", "失败", "报错", "闪退")):
        return "bug"
    if any(keyword in feedback for keyword in ("慢", "加载", "卡", "体验", "不方便")):
        return "experience"
    if any(keyword in feedback for keyword in ("希望", "增加", "新增", "建议")):
        return "feature_request"
    return "other"


def build_priorities(items: list[dict], category_counts: Counter) -> list[dict]:
    priorities = []

    for item in items:
        priority, reason = get_priority(item, category_counts)
        priorities.append({**item, "priority": priority, "reason": reason})

    return sorted(priorities, key=lambda item: (item["priority"], item["feedback"]))


def get_priority(item: dict, category_counts: Counter) -> tuple[str, str]:
    if item["category"] == "bug" and any(
        keyword in item["feedback"] for keyword in ("无法", "失败", "报错", "闪退")
    ):
        return "P0", "影响核心流程，建议优先处理。"
    if category_counts[item["category"]] >= 2:
        return "P1", "同类反馈较多，建议纳入近期规划。"
    return "P2", "单条反馈，建议持续观察。"
