from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CollectionCreate(BaseModel):
    name: str
    parent_id: Optional[str] = None 

class CollectionOut(BaseModel):
    id: str
    name: str
    parent_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    children: List['CollectionOut'] = []

    class Config:
        orm_mode = True

CollectionOut.model_rebuild()