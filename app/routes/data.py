from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, File
from sqlalchemy.orm import Session
from typing import List, Optional

from app.services.database import get_db
from app.middleware.auth import get_current_user
from app.schemas.data import DataCreate, DataOut
from app.models.data import Data
from app.services.s3 import upload_file
from app.services.history import save_history
from app.utils.uuid import generate_uuid
from app.utils.datetime import get_current_timestamp

router = APIRouter()

@router.post("/data", response_model=DataOut)
def create_data(
    data: DataCreate,
    file: Optional[UploadFile] = File(None),
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verifica se collection_id pertence ao usuário para segurança
    if data.collection_id:
        from app.models.collection import Collection
        collection = db.query(Collection).filter(
            Collection.id == data.collection_id,
            Collection.user_id == user_id
        ).first()
        if not collection:
            raise HTTPException(status_code=400, detail="Coleção inválida ou não pertence ao usuário")

    db_data = Data(
        id=generate_uuid(),
        user_id=user_id,
        collection_id=data.collection_id,
        content=data.content,
        file_key=None,
        data_metadata=data.data_metadata,
        created_at=get_current_timestamp(),
        updated_at=get_current_timestamp()
    )
    if file:
        db_data.file_key = upload_file(file, user_id, db_data.id)

    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@router.get("/data", response_model=List[DataOut])
def list_data(
    collection_id: Optional[str] = None,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Data).filter(Data.user_id == user_id)
    if collection_id:
        query = query.filter(Data.collection_id == collection_id)
    return query.all()

@router.put("/data/{id}", response_model=DataOut)
def update_data(
    id: str,
    data: DataCreate,
    file: Optional[UploadFile] = File(None),
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_data = db.query(Data).filter(Data.id == id, Data.user_id == user_id).first()
    if not db_data:
        raise HTTPException(status_code=404, detail="Dado não encontrado")

    # Verifica se nova collection_id pertence ao usuário
    if data.collection_id:
        from app.models.collection import Collection
        collection = db.query(Collection).filter(
            Collection.id == data.collection_id,
            Collection.user_id == user_id
        ).first()
        if not collection:
            raise HTTPException(status_code=400, detail="Coleção inválida ou não pertence ao usuário")

    save_history(db, db_data.id, db_data.content, db_data.file_key, db_data.data_metadata)

    db_data.content = data.content
    db_data.data_metadata = data.data_metadata
    db_data.collection_id = data.collection_id
    db_data.updated_at = get_current_timestamp()

    if file:
        db_data.file_key = upload_file(file, user_id, db_data.id)

    db.commit()
    db.refresh(db_data)
    return db_data

@router.delete("/data/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data(
    id: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_data = db.query(Data).filter(Data.id == id, Data.user_id == user_id).first()
    if not db_data:
        raise HTTPException(status_code=404, detail="Dado não encontrado")

    db.delete(db_data)
    db.commit()

