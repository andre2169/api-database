from sqlalchemy import Column, String, JSON, DateTime, ForeignKey
from app.services.database import Base
from datetime import datetime, timezone

class Data(Base):
    __tablename__ = "data"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    content = Column(JSON)
    file_key = Column(String, nullable=True)
    data_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))