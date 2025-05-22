import pandas as pd # type: ignore
from app.models.data import Data
from sqlalchemy.orm import Session

def export_to_json(db: Session, user_id: str):
    data = db.query(Data).filter(Data.user_id == user_id).all()
    return [d._dict_ for d in data]

def export_to_csv(db: Session, user_id: str):
    data = db.query(Data).filter(Data.user_id == user_id).all()
    df = pd.DataFrame([d._dict_ for d in data])
    return df.to_csv(index=False)