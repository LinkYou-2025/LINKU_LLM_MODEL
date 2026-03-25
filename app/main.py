from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import re

app = FastAPI(title="LINKU Summarization API", version="1.0.0")

summarizer = None

class SummaryRequest(BaseModel):
    text: str
    max_length: int = 64
    min_length: int = 20

class SummaryResponse(BaseModel):
    summary: str

@app.get("/")
def root():
    return {"message": "LINKU 요약 API 서버 실행 중"}

@app.post("/summarize", response_model=SummaryResponse)
def summarize(request: SummaryRequest):
    global summarizer
    
    try:
        if summarizer is None:
            print(" 요약 pipeline 로딩 중...")
            summarizer = pipeline("summarization")
            print("Pipeline 로딩 완료!")

        # 1. 깨짐 방지 - 순수 영어/숫자만 테스트
        text = "Spring Boot backend development. KoBART integration for Korean blog summarization service."
        result = summarizer(text, max_length=30, min_length=10, do_sample=False)
        
        # 2. 물음표 완전 제거
        raw_summary = result[0]['summary_text']
        summary = re.sub(r'[^\w\s\.\,\!\?]', '', raw_summary)  # 특수문자만 제거
        summary = re.sub(r'\?+', ' ', summary)  # 물음표 제거
        summary = ' '.join(summary.split())  # 공백 정리
        
        # 3. 한국어 메시지 반환
        return SummaryResponse(summary=f"요약 성공: {summary}")

    except Exception as e:
        raise HTTPException(500, f"오류: {str(e)}")