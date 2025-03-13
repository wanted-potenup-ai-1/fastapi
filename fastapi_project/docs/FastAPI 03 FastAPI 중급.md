---
title: 📄 [FastAPI] 03 FastAPI 중급
category:
  - PYTHON
date: 2025-03-09 12:54
tags:
  - FastAPI
  - 통신
---
![](https://www.dropbox.com/scl/fi/gcpzyxxk66ro3qeylc7h4/thumbnail_fastapi.png?rlkey=nes5rkrzls0w3ct79rqvnmy66&st=57dyseyn&dl=1)

## 1. 폴더 구조
### 1) 모듈

* 함수와 변수를 포함하는 코드 집합을 담은 `.py` 파일을 **모듈(Module)** 이라고 한다. 
* 여러 개의 모듈을 포함하는 폴더를 **패키지(Package)** 라고 하는데, 패키지 폴더에는 `__init__.py` 파일이 존재한다. 
	* 폴더에 `__init__.py`가 있으면 Python이 폴더를 패키지라고 인식한다.
	* 빈 파일로 둬도 되지만, 패키지 초기 설정, 모듈 가져오기 등을 수행할 수 있다.
* 모듈의 모든 변수, 함수를 불러오고 싶을 때에는 `from module import *`로 표현할 수 있다.

예시로 다음과 같은 폴더 구조가 있다고 하자.

```
📁 Project
├── mypackage/            # 패키지 (폴더)
│   ├── __init__.py       # 패키지 초기화 파일
│   ├── module1.py        # 모듈 1
│   └── module2.py        # 모듈 2
└── main.py
```

#### 내부에서 모듈 불러오기(상대경로 사용)

```python
# mypackage/module2.py
from .module1 import var1, myfunc1
from .module1 import *   # module1의 변수, 함수 모두 불러오기 
```

#### 외부에서 모듈 불러오기(절대경로 사용)

```python
# main.py
from mypackage.module2 import var2, myfunc2
from mypackage.module2 import *   # module2의 변수, 함수 모두 불러오기
```

#### `__init__.py`의 쓰임

`__init__.py`에 패키지 안의 모듈들을 미리 import 하면 외부에서 모듈을 불러올 때 더 편하게 불러올 수 있다.

```python
# __init__.py
from .module1 import *
from .module2 import *

# main.py
from mypackage import var1, var2, myfunc1, myfunc2
```

### 2) FastAPI 폴더 구조

### Router 관리하기

여러 개의 엔드포인트를 그룹화하여 관리하는 객체를 **라우터(Router)** 라고 한다. 

`APIRouter`를 사용하면 라우터를 효율적으로 관리할 수 있다. 

예를 들어 다음과 같은 라우터를 계획중이라고 하자. 그러면 총 3개의 라우터로 그룹지어 관리할 수 있다.

```
1. "/"
2. "/items"
	1) GET "/items"
	2) GET "/items/{item_id}"
	3) GET "/items/query"
	4) POST "/items"
3. "/images"
	1) POST "/images/binary"
	2) POST "/images/files"
```

3번을 예시로 표현하면 다음과 같다. 

```python
from fastapi import APIRouter

image_router = APIRouter(prefix="/images", tags=["Image"])

@image_router.post("/binary")
def create_binary_image(file: bytes = File(...)):
	...

@image_router.post("file")
def create_file_image(file: UploadFile = File(...)):
	...

app.include_router(image_router)
```

모든 코드를 완성한 후, Swagger UI(`http://localhost:8000/docs`)에 접속하면 아래와 같이 그룹화 되어 표현된다. 

<div align="center">
	<img src="https://www.dropbox.com/scl/fi/32zoc2v0tdmuqsljtk8y2/FastAPI008.png?rlkey=f6eogd1yazzjhz62gjqo3e7pd&dl=1" width="60%">
</div>

#### 💡 MVC(Model-View-Controller) 

코드를 체계적으로 구조화하고 유지보수를 쉽게하기 위해 만들어진 코드 설계 패턴을 **디자인 패턴**이라고 한다. 그 중 **MVC 패턴** 에 대해 소개하고자 한다. 

* 웹 애플리케이션을 구조적으로 나누는 설계 패턴
* 역할이 분리되어 유지보수가 쉽다. 
* 재사용성과 확장성이 높다.

<table>
	<thead>
		<tr><th>구성 요소</th><th>역할</th><th>예시</th></tr>
	</thead>
	<tbody>
		<tr>
			<td>Model</td>
			<td>데이터 및 비즈니스 로직 관리</td>
			<td>DB, AI 모델 등</td>
		</tr>
		<tr>
			<td>View</td>
			<td>사용자에게 보여지는 화면</td>
			<td>HTML, JSON 등</td>
		</tr>
		<tr>
			<td>Controller</td>
			<td>요청을 처리하고 Model과 View를 연결</td>
			<td>API 라우터 등</td>
		</tr>
	</tbody>
</table>

#### 자주쓰이는 FastAPI 폴더 구조

MVC 패턴을 반영한 폴더 구조의 예시를 소개하려고 한다. 축소된 버전이기 때문에 더 자세히 알고 싶다면 "FastAPI MVC Structure"로 검색하거나 다른 GitHub Repository를 탐색해보길 바란다.

```
fastapi_project/
├── app/
│   ├── core/                # 설정 관련 파일
│   ├── utils/               # 공통적으로 사용할 유틸리티 함수
│   ├── models/              # AI 모델, DB 관련 코드
│   ├── routers/             # API 라우터 (컨트롤러)
│   ├── schemas/             # 데이터 구조 정의 (Pydantic)
│   ├── static/              # 정적 파일(이미지, CSS 등) 저장
│   ├── templates/           # 프론트엔드 HTML 파일
│   └── main.py              # FastAPI 앱 실행 파일
├── requirements.txt         # 필요한 패키지 목록
└── README.md                # 프로젝트 설명
```

## 2. 타입 힌트

