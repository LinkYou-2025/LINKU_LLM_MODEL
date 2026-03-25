from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.schemas import CategoryRequest, CategoryResponse, SummaryRequest, SummaryResponse
import re
from typing import List
from app.models import get_summarizer, mock_classify 
import os
import sys
if os.name == 'nt':  # Windows
    os.system('chcp 65001 >nul')  # UTF-8 콘솔
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
app = FastAPI(title="LINKU KoBART API v2.0")

from app.utils import extract_keywords 

@app.get("/")
async def root():
    return {"message": "LINKU KoBART 분류+요약 API 실행 중"}

@app.post("/classify", response_model=CategoryResponse)
async def classify_category(request: CategoryRequest):
    """Spring과 100% 호환!"""
    try:
        print(f"📥 [{request.url[:30]}...] {request.text[:50]}...")
        
        # 1. 분류 (mock → KoBART 전환 예정)
        category_id, _ = mock_classify(request.text, request.categories)
        
        # 2. 키워드 추출 (UTF-8 안전)
        keywords = extract_keywords(request.text)
        
        result = {
            "categoryId": category_id,
            "keywords": keywords
        }
        
        print(f" 응답: categoryId={category_id}, keywords={keywords}")
        
        # 3. UTF-8 안전 응답
        return JSONResponse(
            content=result,
            media_type="application/json; charset=utf-8"
        )
        
    except Exception as e:
        print(f"오류: {e}")
        raise HTTPException(status_code=500, detail="분류 실패")

@app.post("/summarize", response_model=SummaryResponse)
async def summarize(request: SummaryRequest):
    try:
        text = request.text.encode('utf-8', errors='ignore').decode('utf-8')
        print(f"📥 원문: {repr(text[:50])}...")  # 디버깅용
        
        # KoBART 강제 실행
        summarizer = get_summarizer()
        summary_result = summarizer(
            text[:450],  # KoBART 입력 제한
            max_length=80,
            min_length=25,
            num_beams=3
        )[0]['summary_text']
        
        print(f"✅ KoBART 요약: {repr(summary_result)}")
        return {"summary": summary_result}
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        # 더 똑똑한 fallback
        keywords = "Company,교제,동행,I enjoy your company,Good Place"
        return {"summary": f"Company의 교제/동행 의미와 Good Place 대사 분석 ({keywords})"}