from pydantic import BaseModel

# Modelo para criar um novo usuário
class UserCreate(BaseModel):
    email: str
    password: str

# Modelo de saída de dados de usuário (por exemplo, ao retornar dados do banco)
class UserOut(BaseModel):
    id: str
    email: str

#  login do usuário
class UserLogin(BaseModel):
    email: str
    password: str
