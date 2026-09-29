# AI 用户反馈分析与需求优先级 Agent

一个面向产品助理场景的可演示 MVP：用户粘贴多条模拟反馈后，页面会分类统计问题，并给出 P0、P1、P2 优先级建议。

## 当前能力

- 每行输入一条模拟用户反馈
- 分类为故障/异常、体验问题、功能需求、其他
- P0：影响核心流程的故障
- P1：同一类别达到两条及以上的反馈
- P2：仍需持续观察的单条反馈

## 本地启动

```powershell
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

## 模拟数据

可复制 `data/sample_feedback.txt` 的内容到页面中测试。请不要放入真实用户信息。
