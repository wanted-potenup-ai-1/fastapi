---
title: 📄 [FastAPI] 02 FastAPI 기초
category:
  - PYTHON
date: 2025-03-08 19:30
tags:
  - FastAPI
---
![](https://www.dropbox.com/scl/fi/gcpzyxxk66ro3qeylc7h4/thumbnail_fastapi.png?rlkey=nes5rkrzls0w3ct79rqvnmy66&st=57dyseyn&dl=1)

## 1. FastAPI
### 1) FastAPI

* 빠르고 쉽게 API를 만들 수 있는 Python 웹 프레임워크
* REST API를 개발할 때 많이 쓰인다.
* Documentation이 잘 되어있어 학습 및 활용이 쉽다.
* [공식 홈페이지](https://fastapi.tiangolo.com/ko/)

### 2) FastAPI 특징

* 비동기(Async) 기반으로 동작하여 높은 성능을 제공한다.
* 자동 문서화 기능을 지원하여 API 문서를 자동으로 생성할 수 있다.
* Typing 라이브러리를 사용하여 데이터 타입 힌트를 활용할 수 있기 때문에 직관적이고 가독성 있는 코드를 작성할 수 있다.
* Pydantic 라이브러리를 사용하여 입력 데이터를 자동으로 검증하고, 유효하지 않을 경우 오류를 반환할 수 있다.

## 2. FastAPI 설치 및 실행

### 1) 설치

```
pip install "fastapi[all]"
```

### 2) 기본 코드

아래 코드는 `http://localhost:8000/` 에 접속하면 `home()`함수가 실행된다는 의미이다. 

이때 이 URL을 **엔드포인트(Endpoint)** 라고 한다. 

```python
from fastapi import FastAPI 

app = FastAPI()

@app.get("/")
def home():
    return {"Hello": "World"}
```

### 3) 실행

```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

* `app.main:app`: 파일명(`app/main.py`)의 `FastAPI()`를 저장한 인스턴스 `app`
* `--host`: 어떤 IP에서 실행할 것인지 지정
	* `127.0.0.1`: 로컬에서만 접근 가능
	* `0.0.0.0`: 모든 IP에서 접근 가능
* `--port`: 서버가 실행될 포트(기본 포트: 8000)
* `--reload`: 코드를 변경하면 자동으로 서버를 다시 시작하는 기능(개발 환경 시 사용)

📌 위의 정보대로 서버를 실행하면 서버의 최상위 폴더는 `app`이 된다.
### 4) Swagger UI

`http://localhost:8000/docs`로 접속하면 API 문서를 볼 수 있다. 

![](https://www.dropbox.com/scl/fi/2wo7p9z2wwcgg3dxpwcxm/FastAPI001.png?rlkey=ore3wrr3x4hubpi2n64hkfls9&dl=1)

#### 💡 Swagger UI 활용 팁

![](https://www.dropbox.com/scl/fi/xujp9vusbafaol3ag2ixo/FastAPI001-1.png?rlkey=qjopjwbzhhhehe30pv99fecf9&dl=1)

## 3. 주의할 점

### 1) 자주 만나는 에러 코드

* `400 Bad Request` : 요청이 잘못된 경우
* `404 Not Found` : 요청한 URL이 존재하지 않거나, 해당 경로에 데이터가 없는 경우
* `422 Unprocessable Entity` : 서버에 입력한 데이터가 잘못된 경우
* `500 Internal Server Error` : 서버 내부에서 에러가 발생한 경우

### 2) 경로 설정

* 최상위 폴더: `main.py`가 있는 위치가 아닌 실행 명령어를 입력한 폴더
* 만약 폴더구조가 다음과 같다면, `fastapi-project`에서 FastAPI 서버를 실행했을 때 파일 경로를 다음과 같이 작성해야 한다. 

	```
	📁 fastapi-project
	├── basic
	│   ├── main.py
	│   ├── sample.json
	│   └── static
	│       └──image.jpg
	├── requests_test.ipynb
	└── 강아지.jpeg
	```

```python
from PIL import Image
image = Image.open("basic/static/image.jpg")
```

### 3) 응답 처리

응답을 할 때 서버 내부 코드에서 에러가 발생한 경우 서버가 꺼지게 된다. 이를 피하기 위해 `try-except`를 이용하면 서버를 안정적으로 운영할 수 있다. 

```python
@app.get("/items")
def get_items():
    try:
		실행코드
		return {
			"status": "success",
			"result": data
		}
	except Exception as e:
		print(f"Error: {e}").   # 서버 관리자가 확인하기 위함
		return {
			"status": "failed",
			"message": "서버 내부 오류가 발생했습니다."
		}
```

## 3. 요청, 응답 처리

* 📌 초보자는 GET, POST 먼저 학습하는 것을 추천
* 📌 FastAPi에서는 응답할 때 딕셔너리로 반환하면 자동으로 JSON으로 변환해주지만, 정확하게 JSON으로 반환하고 싶을 때에는 `JSONResponse`를 사용한다.

	```python
	from fastapi.responses import JSONResponse 
	
	@app.get("/item")
	def get_item():
		실행코드
		return JSONResponse(content=data) 
	```

* 📌 서버에서 입력값을 설정할 때 요청을 어떻게 해야 하는지에 집중한다.
* 📌 개발 과정에서는 API URL에 맞춰 요청 코드 작성(`requests_test.ipynb`)를 미리 작성해두면 편리하다.
* 📌 `requests` 라이브러리를 이용할 때 `response`를 원하는 타입에 맞게 사용할 수 있다. 
	* `response.status_code` : 응답 상태 코드(정상: 200)
	* `response.text` : 응답 본문을 **문자열**로 반환
	*  `response.content` : 응답 본문을 바이너리 형태로 반환
	* `response.json()` : 응답 본문을 **딕셔너리/리스트**로 반환
	

### 1) JSON 데이터

#### 데이터 설정

데이터를 다음과 같은 형식으로 저장하고 있다. 이 정보를 `sample.json`으로 저장하자.

```json
[
    {
        "id": 1,
        "name": "Laptop",
        "category": "Electronics",
        "price": 1500
    },
    {
        "id": 2,
        "name": "Smartphone",
        "category": "Electronics",
        "price": 800
    }
]
```

#### GET

##### 🔗 GET /item/all : 모두 조회

```python
# main.py
import json 

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
```

🔄 **요청 테스트**

```python
# requests_test.ipynb
import requests 

api_url = "http://localhost:8000/items/all"
response = requests.get(api_url)

if response.status_code == 200:
	response_dict = response.json()
	print(response_dict["result"])
```

🐛 **오류 확인**

`except` 구문이 잘 작동하는 것을 확인하기 위해 `app/sample.json`을 `sample.json`으로 바꿔보자. 

이처럼 `try-except` 구문을 활용하면 서버에서는 개발자가 오류 원인을 바로 파악할 수 있고, 클라이언트에서도 어디에 문제가 발생한 건지 직관적으로 이해할 수 있다.

<table>
	<thead>
		<th><code>FastAPI 서버</code></th>
		<th><code>클라이언트</code></th>
	</thead>
	<tbody>
		<td><img src="https://www.dropbox.com/scl/fi/1pyhpl90g1bbclxdjlik0/FastAPI003.png?rlkey=6djmfrh8r7ha2lkubrwvqc473&dl=1"></td>
		<td><img src="https://www.dropbox.com/scl/fi/x2pm7yymspe3iw3p15crc/FastAPI002.png?rlkey=r5r0oy4kwjfdk4axp6sxi3d8g&dl=1"></td>
	</tbody>
</table>

##### 🔗 GET /query?category={category}  : 특정 조건 조회

URL에 `?`기호 뒤에 `key=value`의 형태를 `&`로 연결한 것을 **쿼리 스트링** 이라고 한다. 

주로 필터링, 정렬, 페이지네이션 등의 기능을 구현할 때 사용한다. 

```python
# main.py
@app.get("/items/query")
def get_items_by_category(category: str):
    # 데이터 불러오기
    with open("app/sample.json", "r") as file:
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
```

🔄 **요청 테스트**

```python
# requests_test.ipynb
import requests 

category = "Electronics"
api_url = "http://localhost:8000/items/query"
params = {"category": category}
response = requests.get(api_url, params=params)

if response.status_code == 200:
	response_dict = response.json()
	print(response_dict)
else:
	print(response.status_code)
	print(response.text)
```

##### 🔗 GET /items/{item_id}  : 부분 조회

매개변수를 입력할 때 콜론(`:`)과 함께 타입 힌트를 입력할 수 있다. 타입 힌트를 작성하면 코드 가독성이 좋아지고, 잘못된 데이터가 들어왔을 때 오류 코드(422)를 반환하여 데이터를 검증할 수 있다.

아래의 경우에는 "`item_id`은 반드시 `int`로 받아야 한다"는 의미이다.

```python
# main.py
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
```

🔄 **요청 테스트**

```python
# requests_test.ipynb
import requests 

item_id = 2
api_url = f"http://localhost:8000/items/{item_id}"
response = requests.get(api_url)

if response.status_code == 200:
	response_dict = response.json()
	print(response_dict["result"])
else:
	print(response.status_code)
	print(response.text)
```

🐛 **오류 확인**

`HTTPException`이 잘 작동하는지 확인하기 위해 `item_id`를 10으로 설정해보자. 

<table>
	<thead>
		<th><code>FastAPI 서버</code></th>
		<th><code>클라이언트</code></th>
	</thead>
	<tbody>
		<td><img src="https://www.dropbox.com/scl/fi/o2pn6krh471r6o8iht1fg/FastAPI005.png?rlkey=5mm4tuxl88gtiu34i48yw5ms5&dl=1"></td>
		<td><img src="https://www.dropbox.com/scl/fi/p64c4gebf52eb631x9w0i/FastAPI004.png?rlkey=a30vnttnivgsiwejq6ldtfm67&dl=1"></td>
	</tbody>
</table>

#### POST

##### 🔗 POST /items : 새로운 데이터 생성

```python
# main.py
@app.post("/items")
def create_item(item: dict):
	# 데이터 불러오기
    with open("app/sample.json", "r") as file:
        data = json.load(file)

	# 새로운 데이터의 id 생성
    new_item = {}
    new_item["id"] = data[-1]["id"] + 1
	# 입력 데이터와 합치기
	new_item.update(item)
	# 기존 데이터에 업데이트
    data.append(new_item)

	# 데이터 저장하기
    with open("app/sample.json", "w") as file:
        json.dump(data, file, indent=4)
    
    return {
        "status": "success",
        "result": new_item
    }
```

위 코드에서는 `item` 매개변수의 타입 힌트를 `dict`라고 제시했다. 이 경우에는 딕셔너리 형태이면 모두 통과되기 때문에 데이터 형태와 다른 딕셔너리를 입력해도 정상적으로 저장되게 된다.

이처럼 데이터의 형태에 맞지 않는 입력값의 무분별한 저장을 막기 위해 `pydantic` 라이브러리의 `BaseModel`을 사용한다. 가독성을 위해 반복되는 코드는 주석으로만 처리한다. 

아래의 경우에는 입력한 데이터에 `name, category, price`가 반드시 있어야 하며, 그 타입도 따라야 한다. 

```python
class Item(BaseModel):
    name: str
    category: str
    price: float

@app.post("/items")
def create_item(item: Item):
    # JSON 형식을 딕셔너리로 변환
    item = item.model_dump()

    # 데이터 불러오기(위와 동일)
    
	# 새로운 데이터의 id 생성(위와 동일)
    # 입력 데이터와 합치기(위와 동일)
	# 기존 데이터에 업데이트(위와 동일)
	
	# 데이터 저장하기(위와 동일)
    
    return {
        "status": "success",
        "result": new_item
    }
```

🔄 **요청 테스트**

```python
# requests_test.ipynb
import requests 

item_id = 10
api_url = f"http://localhost:8000/items"
data = {
    "name": "Desk Chair",
    "category": "Furniture",
    "price": 200
}
response = requests.post(api_url, json=data)

if response.status_code == 200:
	response_dict = response.json()
	print(response_dict["result"])
else:
	print(response.status_code)
	print(response.text)
```

🐛 **오류 확인**

위의 요청 코드에서 진행한 데이터에서 `price`키를 삭제해보자. 그러면 `422` 오류 코드와 함께 `detail` 키를 가진 딕셔너리가 반환된다. 

이 의미는 "`body`의 `price`가 `missing`되었다"는 의미이다. 

<img src="https://www.dropbox.com/scl/fi/3h5i07zm9i626kgiain01/FastAPI006.png?rlkey=s2qjdqqjxe3kgkcns3o8ydn6c&dl=1">

이번에는 새로운 키 `quantity`를 추가해보자. 이번에는 정상으로 작동되며, 저장될 때 정의하지 않은 `quantity` 키는 저장되지 않은 것을 확인할 수 있다. 

<div align="center">
<img src="https://www.dropbox.com/scl/fi/a32kjxgwdmhjiztorj9o1/FastAPI007.png?rlkey=btyat1eg3tdykz0r0lb4ahiwh&dl=1" width=60%>
</div>

### 2) 이미지 데이터

#### GET

*  일반적으로 **이미지를 직접 전송하기보다 이미지 URL을 제공하는 방식**을 많이 사용한다.
* 클라이언트는 해당 URL을 이용해 이미지를 가져와서 표시한다.
#### POST

##### 🔗 POST /binary-images : 이미지 데이터 생성

```python
# main.py
from fastapi import File
from datetime import datetime

@app.post("/binary-images")
def create_binary_image(file: bytes = File(...)):
    # 파일 크기 확인
    file_size = len(file)
    
    # 파일 저장 경로 설정
    file_dir = "app/resources/"
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
```

🔄 **요청 테스트**

```python
# requests_test.ipynb
import requests 

api_url = "http://localhost:8000/binary-images"

file_path = "강아지.jpeg"
with open(file_path, "rb") as f:
    file_data = f.read()

files = {"file": file_data}
response = requests.post(api_url, files=files)

if response.status_code == 200:
	response_dict = response.json()
	print(response_dict)
else:
	print(response.status_code)
	print(response.text)
```

📌 **바이너리 데이터로 통신할 때의 단점**

* 메모리 사용량 증가: 파일 크기가 클수록 메모리 부담이 커 대용량인 경우 메모리 부족(Out of Memory, OOM)이 발생할 수 있다.
* 파일 메타데이터 부족: 바이너리 데이터에는 파일명, 확장자, MIME 타입 등의 정보가 없어 사용자가 임의로 설정해야 한다.

#### POST

##### 🔗 POST /file-images : 이미지 데이터 생성

```python
# main.py
@app.post("/file-images")
def create_file_image(file: UploadFile = File(...)):
    # 파일 크기 확인
    file_size = file.size
    
    # 파일 저장 경로 설정
    file_dir = "app/resources/"
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_name = f"{now}-{file.filename}"
    
    file_path = file_dir + file_name 
    
    # 파일 저장
    with open(file_path, "wb") as buffer:
       file_bytes = file.file.read()
       buffer.write(file_bytes)

    return {
        "status": "success",
        "file_name": file_name,
        "file_size": file_size
    }
```

📌 **효율적으로 파일 저장하기(`shutil.copyfileobj()`)**

`UploadFile` 형식으로 파일을 받을 경우, `file.file`은 업로드된 파일의 데이터를 담고 있으며,
`type(file.file)`을 출력하면 `<class 'tempfile.SpooledTemporaryFile'>`이 나온다.

`SpooledTemporaryFile` 는 임시 파일을 저장하는 객체로, FastAPI는 이를 활용하여 작은 크기의 파일은 메모리에 저장하고, 일정 크기를 초과하면 디스크에 저장한다.

따라서 `UploadFile`을 사용할 때, 파일을 효율적으로 저장하기 위해 `file.file.read()`보다는 `shutil.copyfileobj()`를 사용하는 것이 좋다. `shutil.copyfileobj()`는 파일을 스트리밍 방식으로 복사하여 메모리 사용을 최소화하면서도 안정적으로 파일을 저장할 수 있다.

```python
# main.py
import shutil 

@app.post("/file-images")
def create_file_image(file: UploadFile = File(...)):
    # 위와 동일
    
    # 파일 저장
    with open(file_path, "wb") as buffer:
		shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "file_name": file_name,
        "file_size": file_size
    }
```

🔄 **요청 테스트**

```python
# requests_test.ipynb
import requests 

api_url = "http://localhost:8000/file-images"

file_path = "강아지.jpeg"
with open(file_path, "rb") as f:
    files = {"file": ("dog_test.jpg", f, "image/jpeg")}
    response = requests.post(api_url, files=files)

if response.status_code == 200:
	response_dict = response.json()
	print(response_dict)
else:
	print(response.status_code)
	print(response.text)
```

