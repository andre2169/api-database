from typing import List, Optional, Dict, Any
from app.models.collection import Collection

def build_collection_tree(collections: List[Collection], parent_id: Optional[str] = None) -> List[Dict[str, Any]]:
    tree = []
    for col in collections:
        if col.parent_id == parent_id:
            node = {
                "id": col.id,
                "name": col.name,
                "created_at": col.created_at,
                "updated_at": col.updated_at,
                "children": build_collection_tree(collections, col.id)  # chamada recursiva
            }
            tree.append(node)
    return tree
