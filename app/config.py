from dotenv import load_dotenv
import os

load_dotenv("C:/my_api/.env") # carregar o .env

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://apibank_owner:npg_8HdJZqywB2xc@ep-billowing-fire-aczpwhwy-pooler.sa-east-1.aws.neon.tech/apibank?sslmode=require") # o endereço do banco
print(f"DATABASE_URL: {DATABASE_URL}")  # print para depurar
SECRET_KEY = os.getenv("SECRET_KEY", "default_fallback_key") # chave para o JWT
ALGORITHM = "HS256" # criptografia do JWT
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "fake_access_key")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY", "fake_secret_key")
S3_BUCKET = os.getenv("S3_BUCKET", "fake_bucket")