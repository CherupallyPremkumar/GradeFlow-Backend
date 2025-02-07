from io import BytesIO

from fastapi import APIRouter, UploadFile, File, Form, Depends
from app.db.database import SessionLocal
from app.models.client import clients
from app.services.s3_service import upload_to_s3
from app.services.resume_parser import extract_text_from_pdf
from app.services.ats_scoring import calculate_ats_score



router = APIRouter()

@router.post("/upload-resume/")
async def upload_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    location: str = Form(...)
):
    session = SessionLocal()

    file_content = await file.read()
    file_url = upload_to_s3(BytesIO(file_content), file.filename)

    # Extract text from PDF
    resume_text = extract_text_from_pdf(file_content)

    if not resume_text:
        return {"score": 0, "error": "Failed to extract text from resume"}

    # Compute ATS Score
    score = calculate_ats_score(resume_text, job_description)

    # Save client details in DB
    session.execute(clients.insert().values(name=name, email=email, location=location))
    session.commit()
    session.close()

    return {"score": score, "resume_url": file_url}

