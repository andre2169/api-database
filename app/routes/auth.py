from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models import User, Data, Collection, DataHistory
from app.services.database import get_db
from app.services.auth import create_user, authenticate_user, create_access_token
from app.schemas.user import UserCreate, UserOut, UserLogin
from app.middleware.auth import get_current_user
from app.utils.utils import delete_file


router = APIRouter()

@router.post("/auth/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já registrado")
    new_user = create_user(db, user.email, user.password)
    return new_user

@router.post("/auth/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_db = authenticate_user(db, user.email, user.password)
    if not user_db:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_access_token({"sub": user_db.email})
    return {"access_token": token, "token_type": "bearer"}

def delete_collections_recursively(db: Session, user_id: str, parent_id: str = None):
    # Buscar coleções que tem parent_id igual ao parâmetro (ou None para raiz)
    collections = db.query(Collection).filter(Collection.user_id == user_id, Collection.parent_id == parent_id).all()
    for collection in collections:
        # Chama recursivamente para subcoleções
        delete_collections_recursively(db, user_id, collection.id)
        # Deletar a coleção atual
        db.delete(collection)

@router.delete("/user", summary="Delete authenticated user and all data")
def delete_user_account(
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user_id = user.id

    # 1. Deletar dados (Data)
    data_items = db.query(Data).filter(Data.user_id == user_id).all()
    for item in data_items:
        if item.file_key:
            delete_file(item.file_key)  # remove do S3
        db.delete(item)

    # 2. Deletar históricos
    db.query(DataHistory).filter(DataHistory.user_id == user_id).delete()

    # 3. Deletar coleções recursivamente
    delete_collections_recursively(db, user_id)

    # 4. Deletar usuário
    db.delete(user)

    db.commit()
    return {"message": f"Usuário '{user.email}' e todos os dados relacionados foram deletados com sucesso."}