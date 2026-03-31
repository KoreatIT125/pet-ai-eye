from ultralytics import YOLO

def train_construction_model():
    """건축현장 위험 감지 모델 학습"""
    model = YOLO('yolov8s.pt')
    
    results = model.train(
        data='../dataset/construction/data.yaml',
        epochs=100,
        imgsz=640,
        batch=16,
        name='construction_detection',
        device=0
    )
    
    return results

if __name__ == '__main__':
    train_construction_model()
