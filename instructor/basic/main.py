# uvicorn basic-v2.main:app --port 8000 --reload
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import shutil
import json 

app = FastAPI()

@app.get(
    path="/",
    summary="홈페이지입니다"
)
def home():
    """
    해당 경로에 대한 구체적인 설명입니다.
    """
    return {"Hello": "World"}

@app.get("/items/all")
def get_items():
    try:
	    # 데이터 불러오기
        with open("basic/sample.json", "r") as file:
            data = json.load(file)
    
        return {
            "status": "success",
            "result": data
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            "status": "error",
            "result": "서버 내부 오류 발생"
        }
    
@app.get("/items/query")
def get_items_by_category(category: str):
    # 데이터 불러오기
    with open("basic/sample.json", "r") as file:
        data = json.load(file)

    # category에 해당하는 데이터 찾기
    item_list = []
    for item in data:
        if item["category"] == category:
            item_list.append(item)

    return {
        "status": "success",
        "count": len(item_list),
        "result": item_list
    }

@app.get("/items/{item_id}")
def get_item(item_id: int):
	# 데이터 불러오기
	with open("basic/sample.json", "r") as file:
		data = json.load(file)

	# item_id에 해당하는 데이터 찾기
	for item in data:
		if item["id"] == item_id:
			return {
				"status": "success",
				"result": item
			}
	
	raise HTTPException(
		status_code=404, 
		detail="item_id에 해당하는 데이터가 없습니다."
	)

class Item(BaseModel):
    name: str
    category: str
    price: float

@app.post("/items")
def create_item(item: Item):
    # JSON 형식을 딕셔너리로 변환
    item = item.model_dump()

    # 데이터 불러오기
    with open("basic/sample.json", "r") as file:
        data = json.load(file)

	# 새로운 데이터의 id 생성
    new_item = {}
    new_item["id"] = data[-1]["id"] + 1
	# 입력 데이터와 합치기
    new_item.update(item)
	# 기존 데이터에 업데이트
    data.append(new_item)

	# 데이터 저장하기
    with open("basic/sample.json", "w") as file:
        json.dump(data, file, indent=4)
    
    return {
        "status": "success",
        "result": new_item
    }

# 🔗 /binary-images
@app.post("/images/binary")
def create_binary_image(file: bytes = File(...)):
    # 파일 크기 확인
    file_size = len(file)
    
    # 파일 저장 경로 설정
    file_dir = "basic/resources/"
    file_name = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_ext = "jpg"
    
    file_path = file_dir + file_name + "." + file_ext

    # 파일 저장
    with open(file_path, "wb") as buffer:
       buffer.write(file)

    return {
        "status": "success",
        "file_name": file_name,
        "file_size": file_size
    }

# 🔗 /file-images
@app.post("/images/file")
def create_file_image(file: UploadFile = File(...)):
    # 파일 크기 확인
    file_size = file.size
    
    # 파일 저장 경로 설정
    file_dir = "basic/resources/"
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_name = f"{now}-{file.filename}"
    
    file_path = file_dir + file_name 

    # 파일 저장
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "file_name": file_name,
        "file_size": file_size
    }
