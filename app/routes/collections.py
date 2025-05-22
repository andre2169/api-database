from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.services.database import get_db
from app.middleware.auth import get_current_user
from app.schemas.collection import CollectionCreate, CollectionOut
from app.models.collection import Collection
from app.models.user import User
from app.utils.tree_builder import build_collection_tree
from app.utils.uuid import generate_uuid
from app.utils.datetime import get_current_timestamp

router = APIRouter()

def get_user_by_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@router.post("/collections", response_model=CollectionOut)
def create_collection(
    collection: CollectionCreate,
    user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, user_email)

    db_collection = Collection(
        id=generate_uuid(),
        user_id=user.id,
        name=collection.name,
        parent_id=collection.parent_id,
        created_at=get_current_timestamp(),
        updated_at=get_current_timestamp()
    )
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection

@router.get("/collections/{parent_id}/subcollections", response_model=List[CollectionOut])
def get_subcollections(
    parent_id: str,
    user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, user_email)

    subcollections = db.query(Collection).filter(
        Collection.parent_id == parent_id,
        Collection.user_id == user.id
    ).all()

    if not subcollections:
        raise HTTPException(status_code=404, detail="Nenhuma subcoleção encontrada.")

    return subcollections

@router.get("/collections", response_model=List[CollectionOut], summary="List all user collections hierarchically")
def list_user_collections(
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    user = get_user_by_email(db, user_email)

    all_collections = db.query(Collection).filter(Collection.user_id == user.id).all()
    collection_tree = build_collection_tree(all_collections)
    return collection_tree

@router.delete("/collections/{collection_id}", summary="Deleta uma coleção e suas subcoleções")
def delete_collection(
    collection_id: str,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    user = get_user_by_email(db, user_email)

    # Busca a coleção pelo ID e valida se pertence ao usuário
    collection = db.query(Collection).filter(
        Collection.id == collection_id,
        Collection.user_id == user.id
    ).first()

    if not collection:
        raise HTTPException(status_code=404, detail="Coleção não encontrada ou não pertence ao usuário.")

    # Função recursiva para excluir a coleção e suas subcoleções
    def delete_recursively(col_id: str):
        subcollections = db.query(Collection).filter(
            Collection.parent_id == col_id,
            Collection.user_id == user.id
        ).all()
        for sub in subcollections:
            delete_recursively(sub.id)  # chamada recursiva

        # Exclui a própria coleção
        db.query(Collection).filter(Collection.id == col_id).delete()

    delete_recursively(collection_id)

    db.commit()
    return {"message": "Coleção e subcoleções excluídas com sucesso."}
