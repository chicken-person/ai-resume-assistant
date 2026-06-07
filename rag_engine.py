# rag_engine.py
"""
RAG + DeepSeek 核心引擎 - 生产级实现
目标：让 LLM 真正理解简历并给出可执行的优化建议
"""
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

# 全局
_embeddings = None
_vectorstore = None
DEFAULT_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "data/chroma_db")


def get_embeddings():
    global _embeddings
    if _embeddings is None:
        print("加载嵌入模型 shibing624/text2vec-base-chinese ...")
        _embeddings = HuggingFaceEmbeddings(
            model_name="shibing624/text2vec-base-chinese",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )
    return _embeddings


def get_vectorstore(persist_directory: str = DEFAULT_PERSIST_DIR):
    global _vectorstore
    if _vectorstore is not None:
        return _vectorstore

    embeddings = get_embeddings()
    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory, exist_ok=True)

    _vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name="resume_collection"
    )
    return _vectorstore


def index_resume(text: str, persist_directory: str = DEFAULT_PERSIST_DIR) -> int:
    """将简历文本切分并存入向量库"""
    global _vectorstore
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=60,
        separators=["\n\n", "\n", "。", "；", "，", " "]
    )
    chunks = splitter.split_text(text)
    docs = [Document(page_content=chunk, metadata={"source": "resume"}) for chunk in chunks]

    vs = get_vectorstore(persist_directory)
    # 清空旧数据
    try:
        vs.delete_collection()
    except Exception:
        pass

    # 重新创建并更新全局
    _vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=get_embeddings(),
        persist_directory=persist_directory,
        collection_name="resume_collection"
    )
    print(f"✅ 简历已索引，共 {len(chunks)} 个片段")
    return len(chunks)


def retrieve_chunks(query: str, k: int = 8) -> List[Document]:
    """检索最相关的简历片段"""
    vs = get_vectorstore()
    return vs.similarity_search(query, k=k)


def get_deepseek_llm(api_key: Optional[str] = None):
    """获取 DeepSeek LLM（免费版优先）"""
    key = api_key or os.getenv("DEEPSEEK_API_KEY")
    if not key:
        raise ValueError("缺少 DEEPSEEK_API_KEY，请在 .env 或界面中配置")

    model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    return ChatOpenAI(
        model=model,
        temperature=0.2,
        api_key=key,
        base_url="https://api.deepseek.com",
        max_tokens=1500
    )


def get_full_resume_text(path: str = "data/extracted_resume.txt") -> str:
    if not os.path.exists(path):
        raise FileNotFoundError("请先上传并解析简历")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ====================== 核心分析函数 ======================

def analyze_resume_for_target_job(
    resume_text: str,
    target_job: str,
    deepseek_key: Optional[str] = None
) -> str:
    """
    使用 DeepSeek 进行深度分析 - 这是项目的核心价值
    输出结构化、可执行的优化建议
    """
    llm = get_deepseek_llm(deepseek_key)

    # 检索关键片段作为上下文
    chunks = retrieve_chunks(target_job + " 优化 建议 不足 量化", k=10)
    context = "\n\n".join([c.page_content for c in chunks])

    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一位顶尖的中文简历优化专家 + ATS 顾问 + 职业教练。

你的目标是帮助应届生把简历从“能看”变成“能投、能过、能面”。

必须遵守：
1. 所有分析和建议**严格基于用户提供的简历原文**，禁止编造经历。
2. 给出**具体可执行**的修改建议，优先提供可直接复制的 bullet point（改写前后对比）。
3. 针对目标岗位，指出**真正缺少的内容**（不是泛泛而谈）。
4. 同时考虑 ATS 关键词、量化成果、STAR 结构、排版可读性。
5. 输出使用清晰的 Markdown 结构，便于用户直接使用。

输出必须包含以下 6 个部分（严格按顺序）：
"""),
        ("human", """【简历原文】
{resume_text}

【目标岗位】
{target_job}

【简历关键片段（供参考）】
{context}

请按以下结构输出高质量分析报告：

### 1. 简历整体诊断
- 当前主要优势（2-4条）
- 当前主要问题和不足（3-6条，具体指出问题）

### 2. 针对「{target_job}」的匹配度分析
- 匹配度评分（满分 100）
- 岗位最看重的 4-5 个能力中，你简历已具备的（引用原文）
- 明显缺失或薄弱的部分

### 3. 必须补充/强化的内容
列出 4-6 条具体建议，每条说明“为什么重要 + 建议怎么写”

### 4. 可直接使用的优化建议（最重要）
按简历板块给出**改写前后对比**（至少 5-8 个 bullet）：
**原表述**：...
**推荐改写**：...
**改写理由**：...

### 5. ATS 优化建议
- 建议加入的关键词（针对该岗位）
- 格式与排版建议

### 6. 最终行动清单
给出 5-7 条用户今天就可以执行的优化动作（带优先级）

请用中文、专业且鼓励的语气输出。""")
    ])

    chain = prompt | llm
    response = chain.invoke({
        "resume_text": resume_text,
        "target_job": target_job,
        "context": context
    })
    return response.content


def chat_with_resume(
    question: str,
    resume_text: str,
    chat_history: List[Dict] = None,
    deepseek_key: Optional[str] = None
) -> str:
    """支持上下文的简历对话"""
    llm = get_deepseek_llm(deepseek_key)
    chat_history = chat_history or []

    # 检索相关内容
    chunks = retrieve_chunks(question, k=6)
    context = "\n\n".join([c.page_content for c in chunks])

    history_text = ""
    for h in chat_history[-4:]:
        history_text += f"{h['role']}: {h['content']}\n"

    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是用户的专属简历优化 AI 助手。
你非常熟悉用户的简历内容。回答时必须：
- 严格基于简历原文
- 如果用户要求改写，提供具体前后对比
- 回答简洁实用，必要时给出行动建议
- 使用中文"""),
        ("human", """简历内容：
{resume_text}

相关片段：
{context}

历史对话：
{history_text}

当前问题：{question}

请给出准确、具体、有帮助的回答。""")
    ])

    chain = prompt | llm
    resp = chain.invoke({
        "resume_text": resume_text,
        "context": context,
        "history_text": history_text,
        "question": question
    })
    return resp.content


def generate_downloadable_report(analysis_content: str, target_job: str) -> str:
    """生成可下载的 Markdown 报告"""
    header = f"""# AI 简历优化报告

**目标岗位**：{target_job}
**生成时间**：{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}

---

"""
    return header + analysis_content + """

---

*本报告由 AI Resume Assistant + DeepSeek 生成，仅供参考。请结合实际情况修改。*
"""