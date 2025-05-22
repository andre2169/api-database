from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verifica a conexão antes de usar
    pool_recycle=300,    # Recicla conexões a cada 5 minutos
    pool_size=5,         # Tamanho do pool de conexões
    max_overflow=10      # Máximo de conexões extras
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()