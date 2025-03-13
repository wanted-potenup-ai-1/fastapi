from fastapi import APIRouter 

main_router = APIRouter(tags=["Main"])

@main_router.get("/")
def home():
    return {"Hello": "World"}

