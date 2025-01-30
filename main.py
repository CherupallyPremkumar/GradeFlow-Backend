import os
from io import BytesIO

import fitz
import boto3
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from fuzzywuzzy import fuzz
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
DATABASE_URL = "postgresql://ats_user:securepassword@localhost/ats_db"

# Initialize S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Setup FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
metadata = MetaData()

clients = Table(
    "clients",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String),
    Column("email", String),
    Column("location", String),
)

metadata.create_all(engine)


@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...), job_description: str = Form(...), name: str = Form(...),
                        email: str = Form(...), location: str = Form(...)):
    session = SessionLocal()

    file_content = await file.read()
    file_stream = BytesIO(file_content)

    # Upload file to S3
    s3_file_path = f"resumes/{file.filename}"
    s3_client.upload_fileobj(file.file, AWS_S3_BUCKET, s3_file_path)
    file_url = f"https://{AWS_S3_BUCKET}.s3.amazonaws.com/{s3_file_path}"

    file_stream.seek(0)
    # Extract text from PDF
    resume_text = ""
    pdf_document = fitz.open(stream=file_stream.read(), filetype="pdf")
    for page in pdf_document:
        resume_text += page.get_text()

    if not resume_text.strip():
        return {"score": 0, "error": "Failed to extract text from resume"}

    # Calculate ATS Score based on projects, experience, and summary
    sections = ["projects", "experience", "summary", "skills"]
    extracted_sections = [section for section in sections if section in resume_text.lower()]
    filtered_resume_text = " ".join(extracted_sections)
    score = fuzz.ratio(filtered_resume_text.lower(), job_description.lower())

    # Save client details to database
    session.execute(clients.insert().values(name=name, email=email, location=location))
    session.commit()
    session.close()

    return {"score": score, "resume_url": file_url}