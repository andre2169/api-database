from sqlalchemy import Column, String, DateTime, ForeignKey
from app.services.database import Base
from datetime import datetime, timezone

class Collection(Base):
    __tablename__ = "collections"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    parent_id = Column(String, ForeignKey("collections.id"), nullable=True)  
    name = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
