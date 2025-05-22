from sqlalchemy import Column, String, JSON, DateTime, ForeignKey
from app.services.database import Base
from datetime import datetime, timezone

class DataHistory(Base):
    __tablename__ = "data_history"
    id = Column(String, primary_key=True, index=True)
    data_id = Column(String, ForeignKey("data.id"), index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    content = Column(JSON)
    data_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))