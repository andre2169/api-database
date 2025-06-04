import pandas as pd
from app.models.data import Data
from sqlalchemy.orm import Session

def export_to_json(db: Session, user_id: str):
    data = db.query(Data).filter(Data.user_id == user_id).all()
    # Convertendo objetos para dicionário
    return [d.__dict__ for d in data]

def export_to_csv(db: Session, user_id: str):
    data = db.query(Data).filter(Data.user_id == user_id).all()
    df = pd.DataFrame([d.__dict__ for d in data])
    return df.to_csv(index=False)
