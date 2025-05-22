from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.services.database import get_db
from app.middleware.auth import get_current_user
from app.models.data import Data
from app.services.s3 import upload_file, get_file_url

router = APIRouter()

@router.post("/data/{id}/upload")
def upload_file_to_data(
    id: str,
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_data = db.query(Data).filter(Data.id == id, Data.user_id == user_id).first()
    if not db_data:
        raise HTTPException(status_code=404, detail="Dado não encontrado")
    db_data.file_key = upload_file(file, user_id, id)
    db.commit()
    return {"file_key": db_data.file_key}

@router.get("/data/{id}/file")
def get_file_url_for_data(
    id: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_data = db.query(Data).filter(Data.id == id, Data.user_id == user_id).first()
    if not db_data or not db_data.file_key:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    url = get_file_url(db_data.file_key)
    return {"url": url}