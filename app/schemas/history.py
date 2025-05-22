from pydantic import BaseModel
from typing import Optional, Dict, Any

class DataHistoryOut(BaseModel):
    id: str
    data_id: str
    user_id: str
    content: Dict[str, Any]
    data_metadata: Optional[Dict[str, Any]]
    created_at: str

    class Config:
        from_attributes = True