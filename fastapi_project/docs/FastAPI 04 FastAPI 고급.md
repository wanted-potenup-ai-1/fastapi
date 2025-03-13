---
title: 📄 [무제]
category:
  - PYTHON
date: 2025-03-13 08:50
tags:
---
![](https://www.dropbox.com/scl/fi/gcpzyxxk66ro3qeylc7h4/thumbnail_fastapi.png?rlkey=nes5rkrzls0w3ct79rqvnmy66&st=57dyseyn&dl=1)


## 1. Sync / Async


<table width="100%">
	<thead>
		<th width="20%">구분</th>
		<th>Sync(동기)</th>
		<th>Async(비동기)</th>
	</thead>
	<tbody>
		<tr>
			<td>특징</td>
			<td>하나의 요청이 끝난 후 다음 요청 처리 가능</td>
			<td>여러 요청을 동시에 처리 가능</td>
		</tr>
		<tr>
			<td>장점</td>
			<td>구현이 간단하고 직관적</td>
			<td>성능이 뛰어나고 빠름</td>
		</tr>
		<tr>
			<td>단점</td>
			<td>요청이 많아지면 속도가 느려지고, 서버가 지연될 수 있음</td>
			<td>구현이 간단하지 않음. async/await의 이해가 필요</td>
		</tr>
		<tr>
			<td>예시</td>
			<td>단순 연산, 간단 조회 등</td>
			<td>DB 조회, AI 추론 등</td>
		</tr>
	</tbody>
</table>


## 2. Socket / WebSocket

Socket과 WebSocket은 모두 클라이언트와 서버 간의 **실시간 통신** 을 가능하게 하는 기술이다.

WebSocket은 HTTP 기반으로 동작하여 웹 환경에 최적화되어 있다는 차이가 있다. FastAPI와 같은 웹 프레임워크에서 기능을 제공한다.

즉, 서버-클라이언트(웹 브라우저)에서 실시간 통신이 필요하면 WebSocket을 사용하고, 서버-서버에서 실시간 통신이 필요하면 Socket을 쓰는 게 좋다.


<table width="100%">
    <thead>
        <tr>
            <th width="20%">구분</th>
            <th>Socket</th>
            <th>WebSocket</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><b>기본 개념</b></td>
            <td>네트워크에서 데이터를 주고받는 기술</td>
            <td>HTTP에서 실시간 양방향 통신을 지원하는 기술</td>
        </tr>
        <tr>
            <td><b>프로토콜</b></td>
            <td>TCP, UDP</td>
            <td>HTTP 기반 (ws://, wss://)</td>
        </tr>
        <tr>
            <td><b>연결 방식</b></td>
            <td>요청 시 연결 후, 필요하면 유지 가능</td>
            <td>한 번 연결하면 지속적으로 유지</td>
        </tr>
        <tr>
            <td><b>데이터 전송 방식</b></td>
            <td>필요할 때마다 데이터를 주고받음</td>
            <td>연결이 유지되는 동안 실시간 데이터 송수신 가능</td>
        </tr>
        <tr>
            <td><b>사용 사례</b></td>
            <td>파일 전송, 원격 제어 등</td>
            <td>채팅, 실시간 알림, 주식 데이터 스트리밍 등</td>
        </tr>
    </tbody>
</table>

### 1) Socket 

#### (1) 서버

##### 서버 설정

```python
# server.py
# 서버 설정
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005

# UDP 소켓 설정
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT)) # 서버가 특정 IP와 포트에서 데이터를 받을 준비
```

##### 요청 받기

`BUFFER_SIZE`는 한 번에 받을 수 있는 최대 데이터 크기(단위: bytes)를 의미한다.

```python
# server.py
BUFFER_SIZE = 8192

request_data, addr = sock.recvfrom(BUFFER_SIZE)
```

그러나 이미지의 크기가 크면 데이터가 잘리거나 손실될 수 있다. 그래서 적절한 `BUFFER_SIZE` 를 설정한 후 쪼개서 가지고 오는 것을 권장한다.

```python
# server.py
# chunk 단위로 데이터 받기
while True:
	chunk, addr = sock.recvfrom(BUFFER_SIZE)
	if chunk == b"END":
		break 
	image_data.append(chunk)
# chunk 병합
image_data = b"".join(image_data)
```

##### 응답 보내기

```python
# server.py 
sock.sendto(response_data, addr) 
```

마찬가지로 큰 데이터를 한 번에 전달할 수 없으므로 chunk 로 쪼개어 전송한다.

```python
# server.py
for i in range(0, len(json_data), BUFFER_SIZE):
	chunk = json_data[i:i + BUFFER_SIZE]
	sock.sendto(chunk, addr)       # 부분 전송
sock.sendto(b"END", addr)          # 전송 종료 신호
```

#### (2) 클라이언트

##### 서버 정보 입력

```python
# client.py
# 서버 정보 입력
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005
BUFFER_SIZE = 8192

# UDP 소켓 정보 입력
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

##### 요청 보내기

```python
# client.py 
sock.sendto(response_data, addr) 
```

```python
# client.py
BUFFER_SIZE = 8192

_, buffer = cv2.imencode(".jpg", frame) # openCV 이미지를 JPG 형식으로 압축
request_data = buffer.tobytes()
for i in range(0, len(request_data), BUFFER_SIZE):
	chunk = request_data[i:i + BUFFER_SIZE]
	sock.sendto(chunk, addr)     # 부분 전송
sock.sendto(chunk, addr)         # 전송 종료 신호
```
##### 응답 받기

```python
# client.py
request_data, addr = sock.recvfrom(BUFFER_SIZE)
```

```python
# client.py
# chunk 단위로 데이터 받기
response_data = []
while True:
	chunk, _ = sock.recvfrom(BUFFER_SIZE)
	if chunk == b"END":
		break 
	response_data.append(chunk)
# chunk 병합
response_data = b"".join(response_data)
response_data = json.loads(response_data)
```

### 2) WebSocket

#### FastAPI 

```python
# main.py
from fastapi import fastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
	await websocket.accept()
	print("WebSocket 연결됨")

	try:
		# 요청 받기
		request = await websocket.receive_text()
		print(f"클라이언트에게 받은 메세지: {request}")
		
		# 응답 전송
		response = "Hello, python"
		await websocket.send_text(response)
	except Exception as e:
		print(f"에러 발생: {e}")
	finally:
		await websocket.close()
		print("WebSocket 연결 종료")
```

#### Client

```python
# client.py
import websockets
import asyncio

WEBSOCKET_API_URL = "ws://127.0.0.1:8002/ws"

async def send_message(request):
    async with websockets.connect(WEBSOCKET_API_URL) as websocket:
        # 메시지 전송
        await websocket.send(request)  
        # 서버 응답 받기
        response = await websocket.recv()  
        return response

# 질문 전송
request = "hello" 
response = asyncio.run(send_message(request))

print("서버 응답:", response)
```

만약 Jupyter Notebook에서 진행한다면 코드를 수정할 필요가 있다.

Python에서 **이벤트 루프(Event Loop)** 는 비동기 코드(async & await)를 관리하고 실행하는 역할을 한다.

`asyncio.run()`은 새로운 이벤트 루프를 생성하고 실행하려고 하는데, Jupyter Notebook은 이미 자체적으로 이벤트 루프를 실행 중이기 때문에, `asyncio.run()`을 사용하면 충돌이 발생하면서 오류가 발생한다.

이 문제를 해결하려면, 기존의 이벤트 루프에서 비동기 코드를 실행할 수 있도록 `nest_asyncio.apply()`를 사용해야 한다.

```python
# requests_test.ipynb
import websockets
import asyncio

WEBSOCKET_API_URL = "ws://127.0.0.1:8002/ws"

async def send_message(question):
    async with websockets.connect(WEBSOCKET_API_URL) as websocket:
        await websocket.send(request)      # 메시지 전송
        response = await websocket.recv()  # 서버 응답 받기
        return response

# 이미 실행 중인 이벤트 루프에서 실행
loop = asyncio.get_event_loop()
response = loop.run_until_complete(send_message(request="hello"))

print("서버 응답:", response)
```


