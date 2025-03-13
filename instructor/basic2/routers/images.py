from fastapi import APIRouter, File, UploadFile
from datetime import datetime 
import shutil

from basic2.schemas.responses import ImageResponse

image_router = APIRouter(prefix="/images", tags=["Image"])

@image_router.post("/binary")
def create_binary_image(file: bytes = File(...)):
    # 파일 크기 확인
    file_size = len(file)
    
    # 파일 저장 경로 설정
    file_dir = "basic2/resources/"
    file_name = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_ext = "jpg"
    
    file_path = file_dir + file_name + "." + file_ext

    # 파일 저장
    with open(file_path, "wb") as buffer:
       buffer.write(file)

    return ImageResponse(
        status="success",
        file_name=file_name,
        file_size=file_size
    )

@image_router.post("/file")
def create_file_image(file: UploadFile = File(...)):
    # 파일 크기 확인
    file_size = file.size
    
    # 파일 저장 경로 설정
    file_dir = "basic2/resources/"
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_name = f"{now}-{file.filename}"
    
    file_path = file_dir + file_name 

    # 파일 저장
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return ImageResponse(
        status="success",
        file_name=file_name,
        file_size=file_size
    )