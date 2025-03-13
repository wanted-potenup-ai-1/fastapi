from pydantic import BaseModel
from typing import Union, List

class ItemResponse(BaseModel):
    status: str 
    result: Union[str, dict]

class ItemQueryResponse(BaseModel):
    status: str
    count: int 
    result: List[dict]

class ImageResponse(BaseModel):
    status: str 
    file_name: str 
    file_size: int