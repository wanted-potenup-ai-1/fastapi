from fastapi import APIRouter, HTTPException
import json 

from basic2.schemas.requests import ItemRequest
from basic2.schemas.responses import ItemResponse, ItemQueryResponse

item_router = APIRouter(prefix="/items", tags=["Item"])

@item_router.get("/all")
def get_items():
    try:
	    # 데이터 불러오기
        with open("basic2/sample.json", "r") as file:
            data = json.load(file)
    
        return {
            "status": "success",
            "result": data
        }
    except Exception as e:
        print(f"Error: {e}")
        return ItemResponse(
             status="error",
             result="서버 내부 오류 발생"
        )

@item_router.get("/query")
def get_items_by_category(category: str):
    # 데이터 불러오기
    print(category)
    with open("basic2/sample.json", "r") as file:
        data = json.load(file)

    # category에 해당하는 데이터 찾기
    item_list = []
    for item in data:
        if item["category"] == category:
            item_list.append(item)

    return ItemQueryResponse(
         status="success",
         count=len(item_list),
         result=item_list
    )

@item_router.get("/{item_id}")
def get_item(item_id: int):
	# 데이터 불러오기
	with open("basic2/sample.json", "r") as file:
		data = json.load(file)

	# item_id에 해당하는 데이터 찾기
	for item in data:
		if item["id"] == item_id:
			return ItemResponse(
                status="success",
                result=item
            )
	
	raise HTTPException(
		status_code=404, 
		detail="item_id에 해당하는 데이터가 없습니다."
	)

@item_router.post("/")
def create_item(item: ItemRequest):
    # JSON 형식을 딕셔너리로 변환
    item = item.model_dump()

    # 데이터 불러오기
    with open("basic2/sample.json", "r") as file:
        data = json.load(file)

	# 새로운 데이터의 id 생성
    new_item = {}
    new_item["id"] = data[-1]["id"] + 1
	# 입력 데이터와 합치기
    new_item.update(item)
	# 기존 데이터에 업데이트
    data.append(new_item)

	# 데이터 저장하기
    with open("basic2/sample.json", "w") as file:
        json.dump(data, file, indent=4)
    
    return ItemResponse(
        status="success",
        result=new_item
    )