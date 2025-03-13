# 실행 명령어: uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
from fastapi import FastAPI, APIRouter, File, UploadFile
from pydantic import BaseModel
from PIL import Image
import io
import torch

from inference.models.model_loader import *

device = "cuda" if torch.cuda.is_available() else "cpu"

app = FastAPI()

@app.get("/")
def root():
    return {"message": "홈페이지입니다."}
#-----------------------------------------
# 🔗 /predict/review_cls

class ReviewData(BaseModel):
    review: str

@app.post(
        "/review_cls",
        summary="리뷰 긍부정 예측",
        description="텍스트를 받아 리뷰의 긍부정을 예측하는 URL입니다."
)
async def predict_text_cls(data: ReviewData):
    encoded_input = tokenizer(
        data.review, 
        max_length = 128,
        padding="max_length",
        truncation=True,
        add_special_tokens=True,
        return_token_type_ids=True,
        return_attention_mask=True,
        return_tensors='pt'
    )
    # print(encoded_input)
    encoded_input = encoded_input.to(device)
    output = bert_model(**encoded_input)
    # print(output)
    result = output.logits.argmax(dim=1).cpu().item()
    labels = {0:"부정", 1:"긍정"}

    return {
        "status": "success",
        "result": labels[result]
    }
#-----------------------------------------
# 🔗 /predict/image_cls

@app.post(
        "/image_cls",
        summary="연예인 분류 예측(파일)",
        description="이미지 파일을 받아 연예인 이미지를 예측하는 URL입니다."
)
async def predict_image_cls_file(file: UploadFile = File(...)):
    image_bytes = await file.read()
    
    # image = Image.open(io.BytesIO(image_bytes))
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    image_transform = data_transform(image).unsqueeze(0)

    labels = {0: "마동석", 1: "유재석", 2:"카리나"}
    with torch.no_grad():
        pred = vgg16_model(image_transform.to(device))
        result = pred.argmax(dim=1).item()

    return {
        "status": "success",
        "result": labels[result]
    }