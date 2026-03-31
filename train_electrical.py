from ultralytics import YOLO

def train_electrical_model():
    """전기설비 위험 감지 모델 학습"""
    model = YOLO('yolov8s.pt')  # Small 모델 (작은 객체 감지에 유리)
    
    results = model.train(
        data='../dataset/electrical/data.yaml',
        epochs=100,
        imgsz=640,
        batch=16,
        name='electrical_detection',
        device=0
    )
    
    return results

if __name__ == '__main__':
    train_electrical_model()
