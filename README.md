# PetMediScan AI - Eye Disease Detection

반려동물 안구질환 진단 AI 모델 서버

## 기술 스택

- **Framework**: FastAPI
- **Language**: Python 3.10
- **Model**: YOLOv8 / ResNet
- **Deep Learning**: PyTorch
- **Image Processing**: OpenCV, Pillow
- **HTTP Client**: httpx

## 진단 가능한 안구질환

1. **결막염 (Conjunctivitis)** - 눈의 결막 염증
2. **백내장 (Cataract)** - 수정체 혼탁
3. **각막염 (Keratitis)** - 각막 염증
4. **녹내장 (Glaucoma)** - 안압 상승으로 인한 시신경 손상

## 프로젝트 구조

```
pet-ai-eye/
├── app/
│   ├── main.py               # FastAPI 앱
│   ├── model.py              # 모델 로드 및 추론
│   ├── preprocessing.py      # 이미지 전처리
│   └── schemas.py            # Pydantic 모델
├── models/
│   ├── yolov8_eye.pt         # 학습된 YOLOv8 모델
│   └── resnet_eye.pth        # 학습된 ResNet 모델
├── data/
│   ├── train/                # 학습 데이터
│   ├── validation/           # 검증 데이터
│   └── test/                 # 테스트 데이터
├── notebooks/
│   ├── train_yolov8.ipynb    # YOLOv8 학습
│   └── train_resnet.ipynb    # ResNet 학습
├── requirements.txt
├── Dockerfile
└── README.md
```

## API 명세

### 안구질환 진단

**POST** `/predict`

Request:
- Content-Type: `multipart/form-data`
- Body: `image` (file)

Response:
```json
{
  "disease": "결막염",
  "confidence": 0.87,
  "description": "눈의 결막에 발생한 염증으로 충혈, 눈곱, 눈물 등의 증상이 나타납니다.",
  "treatment": "수의사 진료가 필요합니다. 항생제 안약으로 치료 가능합니다.",
  "image_url": "/uploads/predicted_image.jpg"
}
```

### 헬스체크

**GET** `/health`

Response:
```json
{
  "status": "ok",
  "model_loaded": true
}
```

## 데이터셋

### 출처
- **AI Hub**: 반려동물 질병 이미지 데이터
- **Kaggle**: Pet Eye Disease Dataset
- **직접 수집**: 수의사 협력 데이터

### 데이터 구조
```
data/
├── train/
│   ├── conjunctivitis/       # 결막염 (500장)
│   ├── cataract/             # 백내장 (500장)
│   ├── keratitis/            # 각막염 (500장)
│   ├── glaucoma/             # 녹내장 (500장)
│   └── normal/               # 정상 (500장)
├── validation/               # 각 클래스 100장
└── test/                     # 각 클래스 100장
```

## 모델 학습

### 1. YOLOv8 학습

```python
from ultralytics import YOLO

# 모델 초기화
model = YOLO('yolov8n.pt')

# 학습
model.train(
    data='data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    name='eye_disease_yolov8'
)
```

### 2. ResNet 학습

```python
import torch
from torchvision import models

# ResNet50 사용
model = models.resnet50(pretrained=True)
model.fc = torch.nn.Linear(2048, 5)  # 5개 클래스

# 학습 코드
# ... (상세 코드는 notebooks/train_resnet.ipynb 참고)
```

## 개발 환경 설정

### 1. 의존성 설치

```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. FastAPI 서버 실행

```bash
# 개발 모드
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000

# 프로덕션 모드
uvicorn app.main:app --host 0.0.0.0 --port 5000 --workers 4
```

### 3. Docker 실행

```bash
docker build -t petmediscan-ai-eye .
docker run -p 5000:5000 petmediscan-ai-eye
```

## 모델 성능

### 평가 지표 (Test Set)

| 질환명 | Accuracy | Precision | Recall | F1-Score |
|--------|----------|-----------|--------|----------|
| 결막염 | 85%      | 0.84      | 0.86   | 0.85     |
| 백내장 | 88%      | 0.87      | 0.89   | 0.88     |
| 각막염 | 82%      | 0.81      | 0.83   | 0.82     |
| 녹내장 | 80%      | 0.79      | 0.81   | 0.80     |
| 정상   | 90%      | 0.91      | 0.89   | 0.90     |

**전체 Accuracy**: 85%

## Git Workflow

### Branch 전략
- `main`: 프로덕션
- `develop`: 개발
- `feature/ai-eye-기능명`: 기능 개발

### Commit Convention
```
feat: 새로운 기능
fix: 버그 수정
model: 모델 업데이트
data: 데이터셋 추가
docs: 문서 수정
```

## 팀 구성원

- AI 개발자 1: 안구질환 모델 학습
- AI 개발자 2: API 서버 구축

## 참고 자료

- [YOLOv8 공식 문서](https://docs.ultralytics.com/)
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [PyTorch 공식 문서](https://pytorch.org/)
- [AI Hub 데이터셋](https://www.aihub.or.kr/)

## 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.
