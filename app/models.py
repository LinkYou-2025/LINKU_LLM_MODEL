# app/models.py (완전 새 버전)
from transformers import BartForConditionalGeneration, PreTrainedTokenizerFast
from typing import Optional
import torch

_model: Optional[BartForConditionalGeneration] = None
_tokenizer: Optional[PreTrainedTokenizerFast] = None

def get_model():
    global _model
    if _model is None:
        _model = BartForConditionalGeneration.from_pretrained("skt/kobart-base-v1")
        _model.eval()  # 평가 모드
    return _model

def get_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        _tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kobart-base-v1")
        # KoBART 특화 설정
        _tokenizer.pad_token = _tokenizer.eos_token
    return _tokenizer