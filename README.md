# AI 用户反馈分析与需求优先级 Agent

一个面向产品助理场景的可演示 MVP：用户粘贴多条模拟反馈后，DeepSeek 会逐条分析反馈，并返回分类、P0/P1/P2 优先级和处理原因。

## 当前能力

- 每行输入一条模拟用户反馈
- 调用 DeepSeek API，要求模型返回结构化 JSON
- 分类为故障/异常、体验问题、功能需求、其他
- P0：核心流程不可用或严重故障
- P1：明显影响体验或多用户问题
- P2：单条需求或低风险问题

## API 配置

本地可通过环境变量配置 `DEEPSEEK_API_KEY`。部署到 Streamlit Community Cloud 时，在 **Advanced settings → Secrets** 中仅填写：

```toml
DEEPSEEK_API_KEY = "your-key-here"
```

不要把真实 API Key 写入代码、README、GitHub 或截图中。仓库已忽略 `.env` 和 `.streamlit/secrets.toml`。

## 本地启动

```powershell
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

## 模拟数据

可复制 `data/sample_feedback.txt` 的内容到页面中测试。请不要放入真实用户信息。
