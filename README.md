# 🐟 AI Model - 북태평양 연어 지능형 양식장

YOLOv8 기반 연어 개체 감지, 크기 측정, 질병 감지 AI 모델 서버

---

## 📋 **목차**

- [개요](#-개요)
- [AI 모델 구조](#-ai-모델-구조)
- [주요 기능](#-주요-기능)
- [API 명세](#-api-명세)
- [설치 및 실행](#-설치-및-실행)
- [모델 학습](#-모델-학습)
- [디렉토리 구조](#-디렉토리-구조)

---

## 🎯 **개요**

본 AI 모델 서버는 **Flask** 기반으로 구축되었으며, **3개의 독립적인 YOLO 모델**을 사용하여 연어 양식장 자동화를 지원합니다.

### **모델 구성**
1. **Salmon Detection Model** - 연어 개체 감지 및 계수
2. **Salmon Size Model** - 크기 측정 (체장, 체고, 중량 예측)
3. **Salmon Health Model** - 질병 및 스트레스 감지

---

## 🏗️ **AI 모델 구조**

### **Lazy Loading 전략**
- **항상 로드**: `salmon_detection.pt` (기본 개체 감지)
- **필요시 로드**: `salmon_size.pt`, `salmon_health.pt`

### **모델 아키텍처**
```
┌─────────────────────────────────┐
│   CCTV 영상 입력 (Frame)        │
└─────────────┬───────────────────┘
              │
    ┌─────────▼─────────┐
    │ Salmon Detection  │  ← 항상 실행
    │   (YOLOv8-seg)    │
    │  - 개체 감지      │
    │  - 마리 수 계수   │
    └─────────┬─────────┘
              │
    ┌─────────▼─────────┐
    │   Salmon Size     │  ← 필요시 실행
    │  - 체장 측정      │
    │  - 체고 측정      │
    │  - 중량 예측      │
    └─────────┬─────────┘
              │
    ┌─────────▼─────────┐
    │  Salmon Health    │  ← 필요시 실행
    │  - 행동 분석      │
    │  - 질병 감지      │
    │  - 스트레스 평가  │
    └───────────────────┘
```

---

## ✨ **주요 기능**

### **1. 연어 개체 감지 (Salmon Detection)**
- **모델**: YOLOv8m-seg (Segmentation)
- **입력**: 수조 CCTV 이미지 (1920×1080)
- **출력**: 
  - Segmentation Mask (개체별 영역)
  - Bounding Box 좌표
  - 개체 수 (마리)
  - 신뢰도 (Confidence)

### **2. 크기 측정 (Salmon Size)**
- **모델**: YOLOv8s-seg + LightGBM
- **입력**: Segmentation 결과
- **출력**:
  - 체장 (Total Length, mm)
  - 포크길이 (Fork Length, mm)
  - 체고 (Body Depth, mm)
  - 중량 (Weight, g) - LightGBM 회귀 예측

### **3. 질병 감지 (Salmon Health)**
- **모델**: YOLOv8s + Tracking
- **입력**: 연속 프레임 (행동 패턴)
- **출력**:
  - 이동 속도 (정상/느림)
  - 군집 행동 (정상/고립)
  - 질병 위험도 (Low/Medium/High)

---

## 📡 **API 명세**

### **Base URL**: `http://localhost:5000`

### **1. Health Check**
```http
GET /health
```

**Response**:
```json
{
  "status": "ok",
  "models_loaded": ["salmon_detection"],
  "timestamp": "2026-04-02T18:30:00+09:00"
}
```

---

### **2. 연어 개체 감지**
```http
POST /api/detect
Content-Type: multipart/form-data
```

**Request**:
```
image: File (JPG/PNG)
```

**Response**:
```json
{
  "success": true,
  "count": 487,
  "detections": [
    {
      "id": 0,
      "bbox": [120, 350, 250, 180],
      "confidence": 0.92,
      "segmentation": "..."
    }
  ],
  "processing_time_ms": 45
}
```

---

### **3. 크기 측정**
```http
POST /api/size
Content-Type: application/json
```

**Request**:
```json
{
  "image": "base64_encoded_image",
  "detections": [
    {
      "bbox": [120, 350, 250, 180],
      "segmentation": "..."
    }
  ]
}
```

**Response**:
```json
{
  "success": true,
  "measurements": [
    {
      "id": 0,
      "total_length_mm": 226,
      "fork_length_mm": 209,
      "body_depth_mm": 46,
      "weight_g": 118,
      "confidence": 0.88
    }
  ],
  "average": {
    "total_length_mm": 223,
    "weight_g": 115
  }
}
```

---

### **4. 질병 감지**
```http
POST /api/health
Content-Type: application/json
```

**Request**:
```json
{
  "frames": ["base64_1", "base64_2", "base64_3"],
  "tank_id": "tank_001"
}
```

**Response**:
```json
{
  "success": true,
  "health_status": {
    "normal_count": 480,
    "suspicious_count": 7,
    "alerts": [
      {
        "fish_id": 23,
        "behavior": "slow_movement",
        "risk_level": "medium",
        "location": [450, 600]
      }
    ]
  }
}
```

---

## 🚀 **설치 및 실행**

### **1. 사전 요구사항**
- Python 3.10+
- CUDA 11.8+ (GPU 사용 시)

### **2. 가상환경 생성**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### **3. 의존성 설치**
```bash
pip install -r requirements.txt
```

### **4. 모델 다운로드**
```bash
# YOLOv8 사전 학습 모델 다운로드
python download_models.py
```

### **5. 서버 실행**
```bash
python inference_server.py
```

**접속**: http://localhost:5000

---

## 📚 **모델 학습**

### **1. 데이터 준비**
```bash
# dataset Repository에서 AI Hub 데이터 변환
cd ../dataset
python convert_aihub_to_yolo.py --input ./aihub_data --output ./yolo_data
```

### **2. Salmon Detection 모델 학습**
```bash
python train_salmon_detection.py \
  --data ../dataset/salmon_detection/data.yaml \
  --epochs 100 \
  --batch 16 \
  --imgsz 640 \
  --device 0
```

### **3. Salmon Size 모델 학습**
```bash
python train_salmon_size.py \
  --data ../dataset/salmon_size/data.yaml \
  --epochs 100 \
  --batch 16 \
  --imgsz 640
```

### **4. Salmon Health 모델 학습**
```bash
python train_salmon_health.py \
  --data ../dataset/salmon_health/data.yaml \
  --epochs 100 \
  --batch 16 \
  --imgsz 640
```

---

## 📁 **디렉토리 구조**

```
ai-model/
├── models/                     # 학습된 모델 저장
│   ├── salmon_detection.pt
│   ├── salmon_size.pt
│   └── salmon_health.pt
├── utils/                      # 유틸리티 함수
│   ├── __init__.py
│   ├── image_processing.py    # 이미지 전처리
│   └── size_estimation.py     # 크기 측정 알고리즘
├── inference_server.py         # Flask API 서버 (메인)
├── train_salmon_detection.py  # Detection 모델 학습
├── train_salmon_size.py        # Size 모델 학습
├── train_salmon_health.py      # Health 모델 학습
├── download_models.py          # 사전 학습 모델 다운로드
├── requirements.txt            # Python 의존성
├── Dockerfile                  # Docker 이미지 빌드
├── Jenkinsfile                 # CI/CD 파이프라인
└── README.md                   # 본 문서
```

---

## 🔧 **설정 파일**

### **config.yaml**
```yaml
models:
  detection:
    path: models/salmon_detection.pt
    confidence: 0.5
    iou_threshold: 0.45
  
  size:
    path: models/salmon_size.pt
    min_area: 1000  # 최소 픽셀 영역
  
  health:
    path: models/salmon_health.pt
    tracking_frames: 30  # 추적 프레임 수

server:
  host: 0.0.0.0
  port: 5000
  debug: false
```

---

## 📊 **성능 지표 (예상)**

| 모델 | mAP@50 | mAP@50-95 | 추론 속도 (GPU) |
|------|--------|-----------|----------------|
| Salmon Detection | 85%+ | 70%+ | ~25ms/frame |
| Salmon Size | 80%+ | 65%+ | ~30ms/frame |
| Salmon Health | 75%+ | 60%+ | ~35ms/frame |

**테스트 환경**: NVIDIA RTX 3080, CUDA 11.8, cuDNN 8.6

---

## 🐳 **Docker 실행**

### **이미지 빌드**
```bash
docker build -t salmon-ai:latest .
```

### **컨테이너 실행**
```bash
docker run -d \
  --name salmon-ai \
  --gpus all \
  -p 5000:5000 \
  -v $(pwd)/models:/app/models \
  salmon-ai:latest
```

---

## 🧪 **테스트**

```bash
# 단위 테스트
pytest tests/

# API 테스트
python tests/test_api.py
```

---

## 📝 **라이선스**

MIT License - [LICENSE](../LICENSE) 참조

---

## 📞 **문의**

- Issues: [AI Model Issues](https://github.com/KoreanIT125/ai-model/issues)
- Discussions: [Organization Discussions](https://github.com/orgs/KoreanIT125/discussions)

---

**🐟 AI로 연어 양식의 미래를 만듭니다!**
