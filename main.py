# main.py
"""
FastAPI 后端（可选）
提供 REST API，便于未来扩展或移动端调用
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

from resume_parser import process_resume
from rag_engine import (
    index_resume,
    get_full_resume_text,
    analyze_resume_for_target_job,
    chat_with_resume
)

app = FastAPI(title="AI Resume Assistant API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    target_job: str
    deepseek_key: Optional[str] = None

class ChatRequest(BaseModel):
    question: str
    target_job: str
    history: list = []
    deepseek_key: Optional[str] = None

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "仅支持 PDF 文件")

    content = await file.read()
    result = process_resume(content)

    chunks = index_resume(result["text"])
    return {
        "message": "简历解析并索引成功",
        "length": result["length"],
        "chunks": chunks
    }

@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    try:
        text = get_full_resume_text()
        report = analyze_resume_for_target_job(text, req.target_job, req.deepseek_key)
        return {"report": report}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        text = get_full_resume_text()
        answer = chat_with_resume(
            req.question, 
            text, 
            chat_history=req.history,
            deepseek_key=req.deepseek_key
        )
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/health")
async def health():
    return {"status": "ok", "deepseek_configured": bool(os.getenv("DEEPSEEK_API_KEY"))}