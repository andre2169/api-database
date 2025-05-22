from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.database import get_db
from app.middleware.auth import get_current_user
from app.services.export import export_to_json, export_to_csv

router = APIRouter()

@router.get("/data/export")
def export_data(
    format: str, 
    user_id: str = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    if format == "json":
        return export_to_json(db, user_id)
    elif format == "csv":
        return export_to_csv(db, user_id)
    raise HTTPException(status_code=400, detail="Formato inválido")
