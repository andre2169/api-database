from pydantic import BaseModel
from typing import Optional, Dict, Any

class DataCreate(BaseModel):
    content: Dict[str, Any]
    data_metadata: Optional[Dict[str, Any]] = None

class DataOut(BaseModel):
    id: str
    user_id: str
    content: Dict[str, Any]
    file_key: Optional[str]
    data_metadata: Optional[Dict[str, Any]]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True