from ultralytics import YOLO

def train_behavior_model():
    """이상행동 감지 모델 학습"""
    model = YOLO('yolov8m.pt')  # Medium 모델
    
    results = model.train(
        data='../dataset/behavior/data.yaml',
        epochs=100,
        imgsz=640,
        batch=16,
        name='behavior_detection',
        device=0  # GPU 사용
    )
    
    return results

if __name__ == '__main__':
    train_behavior_model()
