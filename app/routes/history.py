from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.database import get_db
from app.middleware.auth import get_current_user
from app.models.history import DataHistory
from app.schemas.history import DataHistoryOut


router = APIRouter()

@router.get("/history", response_model=list[DataHistoryOut])
def list_history(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(DataHistory).filter(DataHistory.user_id == user_id).all()

@router.delete("/history/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_history(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    Datahistory = db.query(DataHistory).filter(DataHistory.id == id, DataHistory.user_id == user.id).first()
    if not Datahistory:
        raise HTTPException(status_code=404, detail="History entry not found")

    db.delete(Datahistory)
    db.commit()
    return