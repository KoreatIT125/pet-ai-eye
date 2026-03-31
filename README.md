# AI Model - Disaster Safety System

YOLOv8 기반 다중 모델 시스템

## 🚀 Tech Stack

- **Python 3.10+**
- **YOLOv8** (Ultralytics)
- **PyTorch 2.0+**
- **Flask** (Inference Server)
- **OpenCV**

## 📦 Models

### 1. Behavior Detection (이상행동 감지)
- **모델**: YOLOv8m
- **클래스**: 넘어짐, 싸움, 침입, 누워있음, 달리기
- **용도**: 모든 CCTV에서 실행 (공통)

### 2. Electrical Equipment (전기설비 위험)
- **모델**: YOLOv8s
- **클래스**: 노출 전선, 스파크, 과열, 전기 연기, 누수
- **용도**: 전기실 CCTV 전용

### 3. Construction Site (건축현장 위험)
- **모델**: YOLOv8s
- **클래스**: 안전모 미착용, 안전조끼 미착용, 낙하물, 불안정 비계, 위험구역
- **용도**: 건축현장 CCTV 전용

## 📦 Setup

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Download Pre-trained Weights

```bash
# YOLOv8 공식 가중치 다운로드
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8m.pt
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt
```

## 🎓 Training

### Behavior Detection

```bash
python train_behavior.py
```

### Electrical Equipment

```bash
python train_electrical.py
```

### Construction Site

```bash
python train_construction.py
```

## 🚀 Inference Server

### Run Server

```bash
python inference_server.py
```

→ http://localhost:5000

### API Endpoints

#### Health Check

```bash
GET /health
```

#### Predict

```bash
POST /predict
- image: file
- cctvType: electrical_room | construction_site | general

Response:
{
  "status": "success",
  "cctvType": "electrical_room",
  "results": {
    "behavior": [...],
    "electrical": [...]
  },
  "alerts": [
    {
      "type": "전기 위험",
      "severity": "high",
      "description": "노출된 전선 감지",
      "confidence": 0.85
    }
  ]
}
```

## 🐳 Docker

```bash
docker build -t safety-ai-model .
docker run --gpus all -p 5000:5000 safety-ai-model
```

## 📁 Project Structure

```
ai-model/
├── train_behavior.py         # 이상행동 모델 학습
├── train_electrical.py       # 전기설비 모델 학습
├── train_construction.py     # 건축현장 모델 학습
├── inference_server.py       # Flask API 서버
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
└── models/                   # 학습된 모델 저장
    ├── behavior.pt
    ├── electrical.pt
    └── construction.pt
```

## 🎯 Architecture

```
CCTV Stream
    ↓
Inference Server (Flask)
    ↓
Router (CCTV 타입 확인)
    ↓
┌──────────┬──────────┬──────────┐
│ Behavior │Electrical│Construction│
│  Model   │  Model   │   Model   │
└──────────┴──────────┴──────────┘
    ↓
Result Aggregator
    ↓
Alert System
```

## 🧪 Testing

```bash
pytest tests/
```

## 📊 Performance

| Model | mAP@0.5 | FPS (GPU) | Size |
|-------|---------|-----------|------|
| Behavior | 0.85 | 60 | 50MB |
| Electrical | 0.78 | 80 | 25MB |
| Construction | 0.81 | 80 | 25MB |

## 📝 License

MIT
