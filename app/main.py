from fastapi import FastAPI, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.routes import auth, collections, data, files, history, export  # ,integrations

app = FastAPI(swagger_ui_parameters={
    "defaultModelsExpandDepth": -1,
    "operationsSorter": "alpha",
})

security = HTTPBearer()

app.include_router(auth)
app.include_router(collections)
app.include_router(data)
app.include_router(files)
app.include_router(history)
app.include_router(export)
# app.include_router(integrations)  Descomente se for usar

@app.get("/")
def read_root():
    return {"message": "API is running"}
