# test_rag.py
"""
RAG 引擎增强测试
测试检索 + 智能问答（支持 LLM 增强 / 回退模式）
"""
from rag_engine import (
    get_full_resume_text,
    retrieve_relevant_chunks,
    answer_question,
    rebuild_index_from_text,
    get_vectorstore
)


def test_retrieval():
    print("\n" + "=" * 60)
    print("【测试 1】纯检索 - Top 相关片段")
    print("=" * 60)
    questions = [
        "教育背景是什么？主修了哪些课程？",
        "有哪些实习或项目经验？",
        "技能特长和语言能力？",
        "适合什么类型的岗位或职业方向？"
    ]
    for q in questions:
        print(f"\n🔍 问题: {q}")
        docs = retrieve_relevant_chunks(q, k=3)
        for i, d in enumerate(docs, 1):
            print(f"  [{i}] {d.page_content[:180]}...")
        print("-" * 40)


def test_rag_answer():
    print("\n" + "=" * 60)
    print("【测试 2】RAG 智能问答（带上下文生成）")
    print("=" * 60)
    test_questions = [
        "请用一句话总结这个人的核心优势。",
        "这个候选人做过哪些量化成果？",
        "如果申请法务/合规/涉外岗位，简历里最匹配的点是什么？",
        "简历还有哪些可以优化的地方？"
    ]
    for q in test_questions:
        result = answer_question(q, k=4)
        print(f"\n❓ {q}")
        print(f"🤖 使用LLM: {result['used_llm']}")
        print("📝 回答:")
        print(result["answer"][:900])
        print("---")


def test_rebuild():
    print("\n" + "=" * 60)
    print("【测试 3】模拟重建索引（使用当前 extracted_resume）")
    print("=" * 60)
    try:
        text = get_full_resume_text()
        info = rebuild_index_from_text(text)
        print(f"✅ 重建成功！索引块数: {info.get('chunks_indexed')}")
    except Exception as e:
        print(f"重建测试跳过或失败: {e}")


if __name__ == "__main__":
    print("🚀 AI Resume Assistant - RAG 模块测试")
    try:
        # 确保向量库就绪
        try:
            get_vectorstore()
        except FileNotFoundError:
            print("检测到无向量库，先执行重建...")
            text = get_full_resume_text()
            rebuild_index_from_text(text)

        test_retrieval()
        test_rag_answer()
        # test_rebuild()  # 可选，取消注释会强制重建
        print("\n✅ 所有测试完成！")
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        print("请确保：")
        print("  1. 已安装依赖: pip install -r requirements.txt")
        print("  2. data/extracted_resume.txt 和 chroma_db 存在（或先运行 resume_parser.py）")
        print("  3. 网络通畅（首次需下载 embedding 模型）")
