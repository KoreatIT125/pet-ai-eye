from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# 모델 로드 (Lazy Loading)
models = {}
model_paths = {
    "behavior": "models/behavior.pt",
    "electrical": "models/electrical.pt",
    "construction": "models/construction.pt"
}

def load_model(model_name):
    """필요할 때만 모델 로드"""
    if model_name not in models:
        print(f"📥 Loading {model_name} model...")
        models[model_name] = YOLO(model_paths[model_name])
    return models[model_name]

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "OK", "message": "AI Model Server Running"})

@app.route('/predict', methods=['POST'])
def predict():
    """이미지 분석 API"""
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    cctv_type = request.form.get('cctvType', 'general')
    
    # 이미지 읽기
    image_file = request.files['image']
    image = Image.open(io.BytesIO(image_file.read()))
    image_np = np.array(image)
    
    # 모델 선택 및 추론
    results = {}
    
    # 이상행동 모델 (항상 실행)
    behavior_model = load_model("behavior")
    behavior_results = behavior_model(image_np)
    results["behavior"] = parse_results(behavior_results[0])
    
    # CCTV 타입별 추가 모델
    if cctv_type == "electrical_room":
        electrical_model = load_model("electrical")
        electrical_results = electrical_model(image_np)
        results["electrical"] = parse_results(electrical_results[0])
    
    elif cctv_type == "construction_site":
        construction_model = load_model("construction")
        construction_results = construction_model(image_np)
        results["construction"] = parse_results(construction_results[0])
    
    # 결과 통합
    alerts = aggregate_alerts(results)
    
    return jsonify({
        "status": "success",
        "cctvType": cctv_type,
        "results": results,
        "alerts": alerts
    })

def parse_results(result):
    """YOLO 결과 파싱"""
    detections = []
    for box in result.boxes:
        detections.append({
            "class": result.names[int(box.cls[0])],
            "confidence": float(box.conf[0]),
            "bbox": box.xyxy[0].tolist()
        })
    return detections

def aggregate_alerts(results):
    """결과 통합 및 알림 생성"""
    alerts = []
    
    # 이상행동 알림
    if "behavior" in results:
        for det in results["behavior"]:
            if det["class"] == "fall_down" and det["confidence"] > 0.8:
                alerts.append({
                    "type": "긴급 상황",
                    "severity": "critical",
                    "description": "넘어짐 감지",
                    "confidence": det["confidence"]
                })
    
    # 전기설비 알림
    if "electrical" in results:
        for det in results["electrical"]:
            if det["class"] == "exposed_wire" and det["confidence"] > 0.6:
                alerts.append({
                    "type": "전기 위험",
                    "severity": "high",
                    "description": "노출된 전선 감지",
                    "confidence": det["confidence"]
                })
    
    # 건축현장 알림
    if "construction" in results:
        for det in results["construction"]:
            if det["class"] == "no_helmet" and det["confidence"] > 0.7:
                alerts.append({
                    "type": "안전장비 미착용",
                    "severity": "medium",
                    "description": "안전모 미착용 감지",
                    "confidence": det["confidence"]
                })
    
    # 우선순위 정렬
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    alerts.sort(key=lambda x: severity_order.get(x["severity"], 999))
    
    return alerts

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
