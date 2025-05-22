# from fastapi import APIRouter, Depends, HTTPException
# from app.middleware.auth import get_current_user
# from app.services.integrations import connect_dropbox

# router = APIRouter()

# @router.post("/integrations/dropbox")
# def connect_dropbox_integration(
#     token: str,
#     user_id: str = Depends(get_current_user)
# ):
#     files = connect_dropbox(token)
#     return files
