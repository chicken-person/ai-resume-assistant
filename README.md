# ai-resume-assistant
基于 LangChain + FastAPI 的 AI 智能简历优化助手（RAG）

一个帮助应届生快速优化简历、模拟面试的 AI 项目，助力月薪 1w+ 就业！

 核心功能
- PDF 简历上传与文本提取
- ATS 匹配度分析 + 优化建议
- 岗位定制化面试模拟
- RAG 知识库（公司面试题 + 行业知识）

 技术栈
- **后端**：Python + FastAPI
- **AI**：LangChain + Sentence-Transformers + Chroma
- **解析**：PyPDF2
- **前端**：Streamlit / Next.js（后续）
- **部署**：Vercel / Render

 项目预览
（后面加上截图）

 快速开始

### 1. 安装依赖
```bash
pip install pypdf2 langchain fastapi uvicorn chromadb sentence-transformers
