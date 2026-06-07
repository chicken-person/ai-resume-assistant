# AI Resume Assistant 🚀

**基于 LangChain + FastAPI + RAG 的智能简历优化与面试助手**

一个帮助计算机本科生快速优化简历、提升 ATS 通过率、模拟面试的 AI 项目。  
助力应届生拿到月薪 1万+ 的心仪 Offer！

---

## ✨ 项目亮点
- 支持 PDF 简历自动解析与文本提取
- 基于 RAG 的智能简历分析与优化建议
- 岗位定制化面试题生成与模拟对话
- ATS（申请人追踪系统）匹配度评分
- 可部署在线 Demo（后续完成）

---

## 🛠️ 技术栈
- **后端**：Python + FastAPI
- **AI 框架**：LangChain
- **向量数据库**：Chroma（本地）
- **嵌入模型**：sentence-transformers（免费）
- **PDF 解析**：pypdf
- **部署**：Vercel / Render / Docker（计划中）

---

## 📂 项目结构
ai-resume-assistant/
├── resume_parser.py          # PDF 解析模块（已完成）
├── rag_engine.py             # RAG 核心引擎（开发中）
├── main.py                   # FastAPI 入口（开发中）
├── frontend/                 # 前端页面（Streamlit 或 Next.js）
├── data/                     # 测试简历和提取结果
├── requirements.txt          # 依赖列表
└── README.md

---

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/你的用户名/ai-resume-assistant.git
cd ai-resume-assistant
2. 安装依赖
Bashpip install -r requirements.txt
3. 运行 PDF 解析测试
Bashpython resume_parser.py
项目截图

如何贡献 / 使用
欢迎 Star ⭐ 和 Fork！
如果你是应届生，欢迎使用本项目优化自己的简历。
有问题请提交 Issue，或直接联系我。
