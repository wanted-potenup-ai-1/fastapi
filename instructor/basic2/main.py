# uvicorn app.main:app --port 8000 --reload

from fastapi import FastAPI
from basic2.routers import *

app = FastAPI()

app.include_router(main_router)
app.include_router(item_router)
app.include_router(image_router)