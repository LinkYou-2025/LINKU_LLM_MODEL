# LINKU-LLM-MODEL

KoBART 기반 블로그 요약 서비스 API 서버

## Features

- KoBART 한국어 요약 모델
- FastAPI + Transformers
- Docker 배포 가능
- Spring Boot와 연동 가능

## Quick Start

```bash
git clone https://github.com/LinkYou-2025/LINKU_LLM_MODEL.git
cd LINKU-LLM-MODEL
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**2. Create a virtual environment (recommended):**
```bash
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Mac/Linux

```

**3. Install dependencies:**

Install the required Python libraries using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```


## API Usage & Testing

서버 실행 후 `http://localhost:8000/docs` (Swagger UI)를 통해 브라우저에서 직접 테스트하거나, 아래의 도구별 예시를 참고하여 호출할 수 있습니다.

### 1. 요약 (Summary)
블로그 본문 등의 긴 텍스트를 핵심 문장으로 요약합니다.

* **Endpoint:** `POST /summarize` (또는 설정된 경로)
* **PowerShell Example:**
```powershell
# 1. UTF8 인코딩 설정
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 2. 테스트 데이터 생성 (JSON 객체)
$summaryData = @{
    text = "Company가 회사의 뜻만 있는 거 아니야? Company는 교제, 동행, 친구 의미도 있습니다! I enjoy your company는 '너와 함께 있어서 즐거워' 표현. Good Place에서 I did enjoy her company는 과거 강조하며 '저도 엘리너와 즐거웠어요' 의미입니다."
} | ConvertTo-Json -Depth 10

# 3. 바이트 배열로 변환 (한글 깨짐 및 유실 방지)
$postParams = [System.Text.Encoding]::UTF8.GetBytes($summaryData)

# 4. API 호출 및 결과 출력
Write-Host "--- 요약 요청 중 (모델 로딩 시 시간이 걸릴 수 있습니다) ---" -ForegroundColor Cyan
$response = iwr -Uri "http://localhost:8000/summarize" `
                -Method Post `
                -Body $postParams `
                -ContentType "application/json"

$response.Content | ConvertFrom-Json | Format-List
```


### 예상 결과
```
{
  "summary": "Company는 교제·동행 의미. I enjoy your company는 함께 있어서 즐겁다는 표현. Good Place에서 과거 강조하며 사용."
}
```


### 2. 분류 (Classify)
텍스트의 내용을 분석하여 해당 포스트의 카테고리를 판별합니다.
* **Endpoint:** `POST /classify` (또는 설정된 경로)
* **PowerShell Example:**
```
$response = iwr -Uri "http://localhost:8000/classify" -Method Post -Body $postParams -ContentType "application/json"
$responseContent = $response | Select-Object -ExpandProperty Content

# 결과 출력
$responseContent
```

## Requirements
최적의 실행을 위해 아래 버전을 권장합니다.
- Python 3.9+
- **NumPy < 2.0.0** (버전 충돌 방지 필수)
- PyTorch >= 2.2.0
- Transformers >= 4.35.0