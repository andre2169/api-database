from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.services.database import Base
from datetime import datetime, timezone

class Collection(Base):
    __tablename__ = "collections"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    parent_id = Column(String, ForeignKey("collections.id"), nullable=True)  # Permite subcoleções
    name = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relacionamentos para facilitar consultas e navegação
    children = relationship("Collection", backref="parent", remote_side=[id])
    data_items = relationship("Data", backref="collection")  # todos os dados vinculados a esta coleção
