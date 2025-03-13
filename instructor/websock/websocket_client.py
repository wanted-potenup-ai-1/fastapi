import websockets
import asyncio

WEBSOCKET_API_URL = "ws://127.0.0.1:8002/ws"

async def send_message(question):
    async with websockets.connect(WEBSOCKET_API_URL) as websocket:
        # 메시지 전송
        await websocket.send(question)  
        # 서버 응답 받기
        response = await websocket.recv()  
        return response

# 질문 전송
question = "반가워요" 
response = asyncio.run(send_message(question))

print("서버 응답:", response)



