"""
🐟 연어 개체 감지 모델 학습 스크립트

YOLOv8 Segmentation 모델을 사용하여 연어 개체를 감지하는 모델 학습

사용법:
    python train_salmon_detection.py --data ../dataset/salmon_detection/data.yaml --epochs 100

Author: KoreanIT125 AI Team
License: MIT
"""

import argparse
from pathlib import Path

# TODO: YOLOv8 import
# from ultralytics import YOLO


def train_detection_model(data_yaml, epochs=100, batch=16, imgsz=640, device=0):
    """
    연어 개체 감지 모델 학습
    
    Args:
        data_yaml (str): YOLO 데이터셋 설정 파일 경로
        epochs (int): 학습 에포크 수
        batch (int): 배치 크기
        imgsz (int): 입력 이미지 크기
        device (int): GPU 장치 번호 (0, 1, ...) 또는 'cpu'
    
    Returns:
        학습된 모델 저장 경로
    
    TODO: 팀원 구현 필요
    1. YOLO 모델 초기화
    2. 학습 진행
    3. 모델 저장
    4. 평가 결과 출력
    """
    print("=" * 50)
    print("🐟 연어 개체 감지 모델 학습 시작")
    print("=" * 50)
    
    # TODO: YOLO 모델 로드
    # model = YOLO('yolov8m-seg.pt')  # Segmentation 모델
    
    # TODO: 학습 시작
    # results = model.train(
    #     data=data_yaml,
    #     epochs=epochs,
    #     batch=batch,
    #     imgsz=imgsz,
    #     device=device,
    #     patience=20,
    #     save=True,
    #     plots=True,
    #     project='runs/salmon_detection',
    #     name='train',
    #     exist_ok=False
    # )
    
    # TODO: 모델 평가
    # metrics = model.val()
    # print(f"mAP50: {metrics.box.map50}")
    # print(f"mAP50-95: {metrics.box.map}")
    
    # TODO: 모델 저장
    # model.export(format='onnx')  # ONNX 형식으로도 저장
    
    print("⚠️ 샘플 스크립트: 팀원이 실제 학습 코드를 구현해야 합니다!")
    print("📖 참고: https://docs.ultralytics.com/modes/train/")
    
    return "models/salmon_detection.pt"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='연어 개체 감지 모델 학습')
    parser.add_argument('--data', type=str, required=True, help='YOLO 데이터셋 YAML 파일 경로')
    parser.add_argument('--epochs', type=int, default=100, help='학습 에포크 수')
    parser.add_argument('--batch', type=int, default=16, help='배치 크기')
    parser.add_argument('--imgsz', type=int, default=640, help='입력 이미지 크기')
    parser.add_argument('--device', default=0, help='GPU 장치 (0, 1, ...) 또는 cpu')
    
    args = parser.parse_args()
    
    # 학습 실행
    model_path = train_detection_model(
        data_yaml=args.data,
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.imgsz,
        device=args.device
    )
    
    print(f"✅ 학습 완료! 모델 저장 위치: {model_path}")
