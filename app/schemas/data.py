from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class DataCreate(BaseModel):
    content: Dict[str, Any]
    data_metadata: Optional[Dict[str, Any]] = None
    collection_id: Optional[str] = None

class DataOut(BaseModel):
    id: str
    user_id: str
    collection_id: Optional[str] = None
    content: Dict[str, Any]
    file_key: Optional[str]
    data_metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
