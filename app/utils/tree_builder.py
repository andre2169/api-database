from typing import List, Dict
from app.schemas.collection import CollectionOut

def build_collection_tree(collections: List) -> List[CollectionOut]:
    collection_dict: Dict[str, CollectionOut] = {}

    # Primeiro converte todas para CollectionOut e cria dicionário por id
    for c in collections:
        collection_dict[c.id] = CollectionOut(
            id=c.id,
            name=c.name,
            parent_id=c.parent_id,
            created_at=c.created_at,
            updated_at=c.updated_at,
            children=[]
        )

    root_collections = []

    # Monta árvore preenchendo children
    for c in collection_dict.values():
        if c.parent_id and c.parent_id in collection_dict:
            collection_dict[c.parent_id].children.append(c)
        else:
            root_collections.append(c)

    return root_collections

