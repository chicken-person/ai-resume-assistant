# AI Resume Assistant

**真正实用、可直接投入使用的 AI 简历优化助手**

针对应届生设计的专业工具：上传 PDF 简历 → 输入目标岗位 → 使用**免费 DeepSeek** 给出**具体可执行**的优化建议和 bullet 改写。

---

## ✨ 核心价值

- 不是泛泛而谈，而是**基于你真实简历内容**的深度诊断
- 针对具体目标岗位，给出**可直接复制的改写建议**（前后对比 + 理由）
- 指出真正缺失的内容（而非模板化建议）
- 支持连续对话追问

---

## 🛠 技术栈

- **LLM**：DeepSeek（deepseek-chat / deepseek-reasoner）—— 免费额度充足，中文极强
- **RAG**：LangChain + Chroma + text2vec-base-chinese
- **解析**：pypdf
- **前端**：Streamlit（简洁专业）
- **后端**：FastAPI（可选）

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd ai-resume-assistant
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 配置 DeepSeek 免费 Key（必须）

1. 打开 [https://platform.deepseek.com/](https://platform.deepseek.com/)
2. 使用微信/手机号注册（新用户送大量免费 Token）
3. 进入 **API Keys** → 创建新 Key
4. 复制 Key（以 `sk-` 开头）

在项目根目录创建 `.env` 文件：

```env
DEEPSEEK_API_KEY=sk-你的免费key
DEEPSEEK_MODEL=deepseek-chat
```

### 3. 启动应用（推荐）

```bash
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`

---

## 使用流程

1. **左侧上传**你的 PDF 简历
2. **输入目标岗位**（例如：法务助理、法院实习生、合规专员）
3. 点击「解析并建立知识库」
4. 去 **📊 深度分析报告** 标签，点击按钮生成专业分析
5. 去 **💬 与简历对话** 进行连续追问和 bullet 改写
6. 最后下载 Markdown 报告

---

## 功能说明

| 功能           | 说明                                      |
|----------------|-------------------------------------------|
| 深度分析报告   | DeepSeek 给出结构化诊断 + 具体改写建议     |
| 智能对话       | 支持上下文追问，可要求改写特定经历         |
| 一键下载报告   | 生成完整 Markdown，可直接用于简历迭代     |
| RAG 检索       | 所有回答都基于你简历真实内容（防幻觉）     |

---

## 常见问题

**Q: DeepSeek 真的免费吗？**  
A: 是的，新注册用户会获得大量免费 Token，个人使用通常足够。

**Q: 分析结果不准确怎么办？**  
A: 确保简历 PDF 文字可提取（扫描件效果差）。多试几次不同目标岗位，效果会更好。

**Q: 可以本地完全免费运行吗？**  
A: 可以。配置好 DeepSeek Key 后，所有分析都在 DeepSeek 免费额度内完成。

**Q: 支持英文简历吗？**  
A: 当前主要优化中文简历（尤其是法律/涉外方向）。英文支持有限。

---

## 项目结构

```
ai-resume-assistant/
├── app.py                 # Streamlit 主界面（推荐入口）
├── main.py                # FastAPI 后端（可选）
├── resume_parser.py       # PDF 解析
├── rag_engine.py          # RAG + DeepSeek 分析核心
├── requirements.txt
├── .env.example
├── README.md
└── data/                  # 简历与向量库存储
```

---

## License

MIT

**Made for 真正需要改简历的应届生**  
希望这个工具能真正帮到你。欢迎反馈使用体验！