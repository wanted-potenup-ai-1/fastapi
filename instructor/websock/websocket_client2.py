import websockets
import asyncio

WEBSOCKET_API_URL = "ws://127.0.0.1:8002/ws/streaming"

async def send_message(question):
    async with websockets.connect(WEBSOCKET_API_URL) as websocket:
        # 메시지 전송
        await websocket.send(question)  
        
        # 서버 응답 받기
        response = ""
        while True:
            token = await websocket.recv()  
            if token == "[END]":
                break
            
            response += token
    
            yield token

# 실행 함수
async def main():
    question = "너에 대해 소개해줘"
    async for token in send_message(question):
        for text in token:
            print(text, end="", flush=True)

# 이벤트 루프 실행
asyncio.run(main())