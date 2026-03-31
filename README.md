# Fish Detection AI Model

YOLO 기반 방어, 부시리, 잿방어 분류 모델

## 🚀 Tech Stack

- Python 3.10+
- Ultralytics YOLOv8
- PyTorch
- OpenCV
- Albumentations (Data Augmentation)

## 📁 Project Structure

```
ai-model/
├── data/
│   └── data.yaml           # YOLO 데이터셋 설정
├── models/
│   ├── yolov8n.pt          # Pre-trained 모델
│   └── best.pt             # 학습된 최고 모델
├── notebooks/
│   ├── eda.ipynb           # 데이터 탐색
│   └── training.ipynb      # 학습 실험
├── scripts/
│   ├── train.py            # 학습 스크립트
│   ├── validate.py         # 검증
│   ├── inference.py        # 추론
│   └── export.py           # 모델 변환 (ONNX 등)
├── utils/
│   ├── augmentation.py     # 데이터 증강
│   └── metrics.py          # 평가 지표
├── requirements.txt
└── README.md
```

## 🛠️ Setup

```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

## 🎯 Training

```bash
# YOLO 학습
python scripts/train.py --data data/data.yaml --epochs 100 --imgsz 640

# 또는 Ultralytics CLI
yolo train data=data/data.yaml model=yolov8n.pt epochs=100 imgsz=640
```

## 📊 Validation

```bash
# 검증
python scripts/validate.py --model models/best.pt --data data/data.yaml

# Ultralytics CLI
yolo val model=models/best.pt data=data/data.yaml
```

## 🔮 Inference

```bash
# 단일 이미지 예측
python scripts/inference.py --model models/best.pt --source path/to/image.jpg

# 배치 예측
python scripts/inference.py --model models/best.pt --source path/to/images/
```

## 📦 Export

```bash
# ONNX 변환 (배포용)
python scripts/export.py --model models/best.pt --format onnx

# TensorFlow Lite 변환 (모바일용)
yolo export model=models/best.pt format=tflite
```

## 📈 Results

학습 결과는 `runs/detect/train/` 폴더에 저장됩니다:
- `weights/best.pt` - 최고 성능 모델
- `results.png` - 학습 곡선
- `confusion_matrix.png` - Confusion Matrix

## 🎯 Classes

```yaml
0: bangeo      # 방어 (Seriola quinqueradiata)
1: busiri      # 부시리 (Seriola lalandi)
2: jaetbangeo  # 잿방어 (Seriola dumerili)
```

## 👥 Team

AI/ML Team

## 📚 References

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [YOLO Documentation](https://docs.ultralytics.com/)
