from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import io
from PIL import Image

app = FastAPI(
    title="PetMediScan AI Eye API",
    version="1.0.0",
    description="반려동물 안구질환 진단 AI 모델 API"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 질환 정보
DISEASES = {
    'conjunctivitis': {
        'name': '결막염',
        'description': '눈의 결막에 발생한 염증으로 충혈, 눈곱, 눈물 등의 증상이 나타납니다.',
        'treatment': '수의사 진료가 필요합니다. 항생제 안약으로 치료 가능합니다.'
    },
    'cataract': {
        'name': '백내장',
        'description': '수정체가 혼탁해져 시력이 저하되는 질환입니다.',
        'treatment': '수술적 치료가 필요할 수 있습니다. 수의사와 상담하세요.'
    },
    'keratitis': {
        'name': '각막염',
        'description': '각막에 염증이 발생하여 통증과 시력 저하가 나타납니다.',
        'treatment': '항생제 치료 및 즉시 수의사 진료가 필요합니다.'
    },
    'glaucoma': {
        'name': '녹내장',
        'description': '안압 상승으로 시신경이 손상되는 질환입니다.',
        'treatment': '응급 치료가 필요하며, 안압 조절 약물 치료를 시행합니다.'
    },
    'normal': {
        'name': '정상',
        'description': '특별한 이상 소견이 관찰되지 않습니다.',
        'treatment': '건강한 상태입니다. 정기적인 검진을 권장합니다.'
    }
}

@app.get("/")
def root():
    """API 루트"""
    return {
        "service": "PetMediScan AI Eye",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    """헬스체크"""
    return {
        "status": "ok",
        "model_loaded": False,  # TODO: 실제 모델 로드 후 True로 변경
        "service": "eye-disease-detection"
    }

@app.post("/predict")
async def predict(image: UploadFile = File(...)):
    """
    안구질환 진단 API
    
    - **image**: 반려동물 안구 이미지 파일
    
    Returns:
        - disease: 진단된 질환명
        - confidence: 신뢰도 (0~1)
        - description: 질환 설명
        - treatment: 치료 방법
    """
    try:
        # 이미지 읽기
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))
        
        # TODO: 실제 YOLOv8 모델 추론
        # 현재는 더미 데이터 반환
        predicted_class = 'conjunctivitis'  # 임시
        confidence = 0.87  # 임시
        
        disease_info = DISEASES.get(predicted_class, DISEASES['normal'])
        
        return {
            "disease": disease_info['name'],
            "confidence": round(confidence, 2),
            "description": disease_info['description'],
            "treatment": disease_info['treatment']
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
