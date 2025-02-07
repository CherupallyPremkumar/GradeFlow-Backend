import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ats_user:securepassword@localhost/ats_db")

settings = Settings()