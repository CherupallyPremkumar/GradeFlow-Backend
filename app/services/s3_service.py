import boto3
from app.core.config import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
)

def upload_to_s3(file_obj, filename):
    s3_client.upload_fileobj(file_obj, settings.AWS_S3_BUCKET, filename)
    return f"https://{settings.AWS_S3_BUCKET}.s3.amazonaws.com/{filename}"