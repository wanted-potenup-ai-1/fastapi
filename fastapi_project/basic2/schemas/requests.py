from pydantic import BaseModel

class ItemRequest(BaseModel):
    name: str
    category: str
    price: float