from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, File
from sqlalchemy.orm import Session
from app.services.database import get_db
from app.middleware.auth import get_current_user
from app.schemas.data import DataCreate, DataOut
from app.models.data import Data
from app.services.history import save_history
from app.services.s3 import upload_file
from app.utils.uuid import generate_uuid
from app.utils.datetime import get_current_timestamp
from typing import List

router = APIRouter()

@router.post("/data", response_model=DataOut)
def create_data(
    data: DataCreate,
    file: UploadFile = File(None),
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_data = Data(
        id=generate_uuid(),
        user_id=user_id,
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

@router.get("/data", response_model=List[DataOut])  # Usando List para tipagem de lista
def list_data(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Data).filter(Data.user_id == user_id).all()

@router.put("/data/{id}", response_model=DataOut)
def update_data(
    id: str,
    data: DataCreate,
    file: UploadFile = File(None),
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_data = db.query(Data).filter(Data.id == id, Data.user_id == user_id).first()
    if not db_data:
        raise HTTPException(status_code=404, detail="Dado não encontrado")
    # Salva o histórico antes de atualizar
    save_history(db, db_data.id, db_data.content, db_data.file_key, db_data.data_metadata)
    # Atualiza os dados
    db_data.content = data.content
    db_data.data_metadata = data.data_metadata
    db_data.updated_at = get_current_timestamp()
    if file:
        db_data.file_key = upload_file(file, user_id, db_data.id)
    db.commit()
    db.refresh(db_data)
    return db_data

@router.delete("/data/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    data = db.query(Data).filter(Data.id == id, Data.owner_id == user.id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")

    db.delete(data)
    db.commit()
    return