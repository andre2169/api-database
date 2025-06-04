from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: str
    email: str

class UserLogin(BaseModel):
    email: str
    password: str
