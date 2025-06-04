from sqlalchemy.orm import Session
from app.models.data import Data
from app.models.history import DataHistory
from app.utils.uuid import generate_uuid
from app.utils.datetime import get_current_timestamp

def save_history(db: Session, data_id: str, content: dict, file_key: str = None, data_metadata: dict = None):
    data_record = db.query(Data).filter(Data.id == data_id).first()
    if not data_record:
        raise ValueError("Data record not found")
    history = DataHistory(
        id=generate_uuid(),
        data_id=data_id,
        user_id=data_record.user_id,
        content=content,
        file_key=file_key,
        data_metadata=data_metadata,
        created_at=get_current_timestamp()
    )
    db.add(history)
    db.commit()
