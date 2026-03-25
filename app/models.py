from transformers import BartForConditionalGeneration, PreTrainedTokenizerFast, pipeline
from typing import Optional, Tuple, List 
import torch
import os

# 전역 싱글톤
_classifier_model: Optional[BartForConditionalGeneration] = None
_classifier_tokenizer: Optional[PreTrainedTokenizerFast] = None
_summarizer: Optional[pipeline] = None

def get_classifier_model_and_tokenizer() -> Tuple[BartForConditionalGeneration, PreTrainedTokenizerFast]:
    """분류 모델 싱글톤 로더"""
    global _classifier_model, _classifier_tokenizer
    if _classifier_model is None:
        print("🔄 KoBART 분류 모델 로딩 중...")
        model_path = "./kobart-category-finetuned"
        if not os.path.exists(model_path):
            model_path = "gogamza/kobart-base-v2"
            
        _classifier_model = BartForConditionalGeneration.from_pretrained(model_path)
        _classifier_tokenizer = PreTrainedTokenizerFast.from_pretrained(model_path)
        _classifier_tokenizer.pad_token = _classifier_tokenizer.eos_token
        _classifier_model.eval()
        print("분류 모델 로딩 완료!")
    
    return _classifier_model, _classifier_tokenizer

def get_summarizer() -> pipeline:
    """요약 pipeline 싱글톤"""
    global _summarizer
    if _summarizer is None:
        print("🔄 요약 pipeline 로딩 중...")
        _summarizer = pipeline("summarization", model="gogamza/kobart-base-v2")
        print("요약 pipeline 로딩 완료!")
    return _summarizer

def mock_classify(text: str, category_ids: List[int]) -> Tuple[int, str]:
    """파인튜닝 전 테스트용"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["여행", "제주", "관광"]):
        if 2 in category_ids: return 2, "#여행 #제주 #관광"
    elif any(word in text_lower for word in ["음식", "레시피", "맛집"]):
        if 3 in category_ids: return 3, "#맛집 #요리 #레시피"
    elif any(word in text_lower for word in ["개발", "프로그래밍", "spring"]):
        if 1 in category_ids: return 1, "#개발 #Spring #코딩"
    
    return 16, "#기타 #일상"