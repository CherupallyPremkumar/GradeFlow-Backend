import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ats_user:securepassword@localhost/ats_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "b1080f0e4a4eeb10e19a99ebc5b25402a552f69c291e0af52bb34ae2eb35ed55")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
settings = Settings()