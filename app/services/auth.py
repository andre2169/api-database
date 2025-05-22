from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
# from app.config import SECRET_KEY, ALGORITHM
from app.models.user import User
from sqlalchemy.orm import Session
from app.utils.uuid import generate_uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Definido diretamente para evitar problemas com a importação
SECRET_KEY = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
ALGORITHM = "HS256"

def create_user(db: Session, email: str, password: str):
    hashed_password = pwd_context.hash(password)
    user = User(id=generate_uuid(), email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    print(f"SECRET_KEY: {SECRET_KEY}, type: {type(SECRET_KEY)}")
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)