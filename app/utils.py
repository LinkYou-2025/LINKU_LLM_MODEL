import re
from typing import List

CATEGORY_KEYWORDS = {
    1: ["IT", "기술", "프로그래밍"],
    2: ["여행", "관광", "휴가"],
    3: ["음식", "레시피", "맛집"],
    16: ["기타", "일상"]
}

def extract_keywords(text: str, top_k: int = 4) -> str:
    """UTF-8 안전 키워드 추출"""
    clean_text = re.sub(r'[^\w가-힣\s]', ' ', text)
    words = re.findall(r'\b[a-zA-Z가-힣]{2,8}\b', clean_text)
    unique = list(dict.fromkeys(words))[:top_k]
    keywords = [f"#{w}" for w in unique]
    return ", ".join(keywords)

def mock_classify(text: str, category_ids: list[int]) -> tuple[int, str]:
    """파인튜닝 전 분류"""
    text_lower = text.lower()
    if any(word in text_lower for word in ["여행", "제주", "관광"]):
        return 2, "#여행"
    elif any(word in text_lower for word in ["음식", "레시피", "맛집"]):
        return 3, "#맛집"
    elif any(word in text_lower for word in ["개발", "spring", "코딩"]):
        return 1, "#개발"
    return 16, "#기타"