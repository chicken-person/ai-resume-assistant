# resume_parser.py
"""
简历 PDF 解析模块 - 生产级
支持上传 PDF，提取干净文本，基础清理。
"""
from pypdf import PdfReader
import os
import re
from typing import Union, BinaryIO
from pathlib import Path


def clean_text(text: str) -> str:
    """清理 PDF 提取的常见噪声"""
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text)
    # 移除特殊 bullet 字符
    text = text.replace('\uf06c', '•').replace('\uf0a7', '•')
    # 清理多余换行
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def extract_text_from_pdf(pdf_path: Union[str, Path]) -> str:
    """从本地 PDF 提取文本"""
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"文件不存在: {pdf_path}")

    reader = PdfReader(str(pdf_path))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"

    return clean_text(text)


def extract_text_from_upload(file: Union[BinaryIO, bytes]) -> str:
    """从上传文件提取文本"""
    from io import BytesIO

    if isinstance(file, (bytes, bytearray)):
        reader = PdfReader(BytesIO(file))
    else:
        reader = PdfReader(file)

    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"

    return clean_text(text)


def process_resume(
    source: Union[str, Path, BinaryIO, bytes],
    save_path: str = "data/extracted_resume.txt"
) -> dict:
    """统一处理简历，返回结构化结果"""
    if isinstance(source, (str, Path)):
        text = extract_text_from_pdf(source)
    else:
        text = extract_text_from_upload(source)

    # 保存
    os.makedirs(os.path.dirname(save_path) or "data", exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(text)

    return {
        "text": text,
        "length": len(text),
        "saved_to": save_path,
        "preview": text[:600] + "..." if len(text) > 600 else text
    }


if __name__ == "__main__":
    # 测试
    result = process_resume("data/test_resume.pdf")
    print("✅ 解析成功")
    print(f"长度: {result['length']}")
    print(result['preview'])