# uvicorn websock.main:app --port 8002 --reload
from fastapi import FastAPI, WebSocket
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()  # 환경 변수 로드

# OpenAI API 설정 (LangChain 사용)
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 사람입니다."),
    ("user", "{input}")  # 사용자 입력을 받을 자리
])
model = ChatOpenAI(model_name="gpt-4o-mini")
output_parser = StrOutputParser()

chain = prompt | model | output_parser

app = FastAPI()

@app.get("/")
def home():
    return {"Hello": "World"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket 연결됨")

    try:
        # 클라이언트 메시지 받기
        data = await websocket.receive_text()  
        print(f"클라이언트 메시지: {data}")

        # LangChain을 이용하여 응답 생성
        response = await chain.ainvoke({"input": data})
        print(response)

        # 응답 전송
        await websocket.send_text(response)  

    except Exception as e:
        print(f"WebSocket 에러 발생: {e}")
    finally:
        await websocket.close()
        print("WebSocket 연결 종료")

@app.websocket("/ws/streaming")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket 연결됨")

    try:
        # 클라이언트 메시지 받기
        data = await websocket.receive_text()  
        print(f"클라이언트 메시지: {data}")

        # LangChain을 이용하여 응답 생성
        response = chain.astream({"input": data})
        print("챗봇 메시지: ", end="")
        async for token in response:
            print(token, end="", flush=True)
            # 응답 전송
            await websocket.send_text(token)
        # 응답 전송(종료 신호)
        await websocket.send_text("[END]")  
        print("")

    except Exception as e:
        print(f"WebSocket 에러 발생: {e}")
    finally:
        await websocket.close()
        print("WebSocket 연결 종료")