import streamlit as st

from src.feedback_analyzer import analyze_feedback


st.set_page_config(page_title="AI 用户反馈分析与需求优先级 Agent", page_icon="🧭")

st.title("AI 用户反馈分析与需求优先级 Agent")
st.write("粘贴模拟用户反馈，获取问题分类与 P0/P1/P2 优先级建议。")

feedback_text = st.text_area(
    "用户反馈（每行一条）",
    placeholder="例如：页面报错无法提交\n希望增加深色模式\n页面加载太慢",
    height=220,
)

if st.button("开始分析", type="primary"):
    if not feedback_text.strip():
        st.warning("请至少输入一条用户反馈。")
    else:
        result = analyze_feedback(feedback_text)
        st.subheader("分析概览")
        st.metric("反馈总数", result["total_count"])

        st.subheader("问题分类统计")
        category_names = {
            "bug": "故障/异常",
            "experience": "体验问题",
            "feature_request": "功能需求",
            "other": "其他",
        }
        for category, count in result["category_counts"].items():
            st.write(f"{category_names[category]}：{count} 条")

        st.subheader("优先级建议")
        for item in result["priorities"]:
            st.markdown(
                f"**{item['priority']}｜{category_names[item['category']]}**："
                f"{item['feedback']}  \n{item['reason']}"
            )
