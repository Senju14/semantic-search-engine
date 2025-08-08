from pydantic import BaseModel
from typing import List, Optional

class Product(BaseModel):
    id: str
    name: str
    description: str
    category: str
    price: Optional[int] = None
    brand: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    tags: Optional[List[str]] = []
    image_path: Optional[str] = None

class SearchQuery(BaseModel):
    query: str
