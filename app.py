# app.py
"""
AI Resume Assistant - Streamlit 主界面
真正实用、专业的简历优化工具
"""
import os
import streamlit as st
from dotenv import load_dotenv

from resume_parser import process_resume
from rag_engine import (
    index_resume,
    get_full_resume_text,
    analyze_resume_for_target_job,
    chat_with_resume,
    generate_downloadable_report
)

load_dotenv()

st.set_page_config(
    page_title="AI Resume Assistant | 智能简历优化助手",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式
st.markdown("""
<style>
    .main-header { font-size: 2.1rem; font-weight: 700; color: #1e3a8a; margin-bottom: 0.3rem; }
    .sub-header { color: #475569; font-size: 1.05rem; margin-bottom: 1.2rem; }
    .success-box { background: #f0fdf4; border: 1px solid #86efac; padding: 1rem; border-radius: 8px; }
    .warning-box { background: #fefce8; border: 1px solid #fde047; padding: 1rem; border-radius: 8px; }
    .metric-card { background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# ====================== Sidebar ======================
with st.sidebar:
    st.title("📄 AI Resume Assistant")
    st.caption("真正能帮你改出好简历的 AI 工具")

    st.divider()

    # DeepSeek 状态 + Key 输入
    deepseek_key = os.getenv("DEEPSEEK_API_KEY") or st.session_state.get("deepseek_api_key", "")
    if deepseek_key:
        st.success("✅ DeepSeek 已连接（免费版）")
    else:
        st.warning("⚠️ 未检测到 DeepSeek Key")
        key_input = st.text_input("粘贴 DeepSeek API Key", type="password", key="key_input")
        if st.button("保存 Key"):
            if key_input.startswith("sk-"):
                st.session_state["deepseek_api_key"] = key_input.strip()
                st.success("Key 已保存到本次会话")
                st.rerun()
            else:
                st.error("Key 格式不正确")

    st.divider()

    # 上传区域
    st.subheader("1. 上传简历")
    uploaded_file = st.file_uploader("上传 PDF 简历", type=["pdf"], label_visibility="collapsed")

    target_job = st.text_input(
        "2. 目标岗位（必填）",
        placeholder="例如：法务助理、法院实习生、合规专员、涉外律师助理",
        value=st.session_state.get("target_job", "")
    )

    if st.button("🚀 解析并建立知识库", type="primary", use_container_width=True):
        if not uploaded_file:
            st.error("请先上传 PDF 简历")
        elif not target_job.strip():
            st.error("请输入目标岗位")
        else:
            with st.spinner("正在解析简历并建立向量索引..."):
                try:
                    # 解析
                    result = process_resume(uploaded_file.getvalue())
                    st.session_state["resume_text"] = result["text"]
                    st.session_state["target_job"] = target_job.strip()

                    # 建立索引
                    chunks = index_resume(result["text"])
                    st.session_state["indexed"] = True

                    st.success(f"✅ 解析成功！共索引 {chunks} 个片段")
                    st.rerun()
                except Exception as e:
                    st.error(f"处理失败: {e}")

    st.divider()

    # 状态
    if st.session_state.get("indexed"):
        st.info(f"当前简历已就绪\n目标岗位：{st.session_state.get('target_job', '未设置')}")
    else:
        st.info("请先上传简历并建立知识库")

    if st.button("清空当前数据", use_container_width=True):
        for key in ["resume_text", "target_job", "indexed", "analysis_report"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    st.divider()
    st.caption("使用 DeepSeek 免费版\n数据仅在本地处理")

# ====================== 主界面 ======================
st.markdown('<p class="main-header">AI Resume Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">上传简历 → 深度分析 → 可执行优化建议 | 专为应届生设计</p>', unsafe_allow_html=True)

if not st.session_state.get("indexed"):
    st.warning("👆 请先在左侧上传你的 PDF 简历并输入目标岗位，然后点击「解析并建立知识库」")
    st.stop()

# 获取数据
resume_text = st.session_state.get("resume_text", "")
target_job = st.session_state.get("target_job", "")
deepseek_key = st.session_state.get("deepseek_api_key") or os.getenv("DEEPSEEK_API_KEY")

# Tabs
tab_analysis, tab_chat, tab_report = st.tabs([
    "📊 深度分析报告", 
    "💬 与简历对话", 
    "📥 下载优化报告"
])

# ====================== Tab 1: 深度分析 ======================
with tab_analysis:
    st.subheader("针对目标岗位的深度诊断与优化建议")

    if st.button("🔍 使用 DeepSeek 生成专业分析报告", type="primary", use_container_width=True):
        if not deepseek_key:
            st.error("请先在 .env 中配置 DEEPSEEK_API_KEY，或在左侧输入 Key")
            st.stop()

        with st.spinner("DeepSeek 正在深度分析你的简历（这可能需要 15-40 秒）..."):
            try:
                report = analyze_resume_for_target_job(
                    resume_text, 
                    target_job, 
                    deepseek_key
                )
                st.session_state["analysis_report"] = report
                st.success("✅ 分析完成！")
            except Exception as e:
                st.error(f"分析失败: {str(e)}")
                st.info("请检查 DeepSeek Key 是否正确，以及网络连接。")

    # 显示报告
    if "analysis_report" in st.session_state:
        st.markdown("---")
        st.markdown(st.session_state["analysis_report"])

        # 下载按钮
        report_md = generate_downloadable_report(
            st.session_state["analysis_report"], 
            target_job
        )
        st.download_button(
            "📥 下载完整 Markdown 报告",
            data=report_md,
            file_name=f"简历优化报告_{target_job}.md",
            mime="text/markdown",
            use_container_width=True
        )

# ====================== Tab 2: 聊天 ======================
with tab_chat:
    st.subheader("与你的简历对话（支持连续追问）")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 示例问题
    st.caption("推荐问题（点击使用）：")
    example_qs = [
        "我的法院/实习经历目前写得怎么样？",
        "针对这个岗位，我最需要补充什么内容？",
        "帮我把普法项目经历改得更有冲击力",
        "这个简历在 ATS 系统里大概能过吗？"
    ]
    cols = st.columns(len(example_qs))
    for i, q in enumerate(example_qs):
        if cols[i].button(q, key=f"ex_{i}", use_container_width=True):
            st.session_state["pending_question"] = q

    # 输入
    question = st.chat_input("输入你的问题，例如：如何改写我的项目经历？")

    if "pending_question" in st.session_state:
        question = st.session_state.pop("pending_question")

    if question:
        if not deepseek_key:
            st.error("请先配置 DeepSeek Key")
        else:
            with st.spinner("思考中..."):
                try:
                    answer = chat_with_resume(
                        question,
                        resume_text,
                        chat_history=st.session_state.chat_history,
                        deepseek_key=deepseek_key
                    )
                    st.session_state.chat_history.append({"role": "user", "content": question})
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"对话失败: {e}")

    # 渲染聊天
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if not st.session_state.chat_history:
        st.info("在左侧配置好 Key 后，可以在这里连续追问简历的任何问题。")

# ====================== Tab 3: 下载报告 ======================
with tab_report:
    st.subheader("一键生成可下载的优化报告")

    if st.button("生成完整优化报告（Markdown）", type="primary"):
        if "analysis_report" not in st.session_state:
            st.warning("请先在「深度分析报告」标签生成分析")
        else:
            report = generate_downloadable_report(
                st.session_state["analysis_report"], 
                target_job
            )
            st.download_button(
                "📥 点击下载 Markdown 文件",
                data=report,
                file_name=f"AI简历优化报告_{target_job.replace(' ', '_')}.md",
                mime="text/markdown"
            )
            st.success("报告已准备好下载！")

    st.info("""
    **提示**：
    - 建议先生成「深度分析报告」，再下载完整版
    - 下载的 Markdown 可以直接复制到 Notion / Word / Typora 使用
    - 报告内容全部基于你的真实简历 + DeepSeek 专业分析
    """)

# Footer
st.divider()
st.caption("AI Resume Assistant v2.0 | 基于 DeepSeek 免费版 + RAG | 数据仅本地处理 | 专为应届生设计")