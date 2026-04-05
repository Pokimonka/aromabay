import os
from fastapi import APIRouter, UploadFile, File
from starlette.responses import JSONResponse
from app.s3cloude import S3Client

router = APIRouter(prefix="/uploads", tags=["uploads"])

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

ACCESS_S3_KEY = os.getenv("ACCESS_S3_KEY")
SECRET_S3_KEY = os.getenv("SECRET_S3_KEY")
ENDPOINT_URL = os.getenv("ENDPOINT_URL")
BUCKET_NAME = os.getenv("BUCKET_NAME")

@router.post('/image')
async def upload_perfume_image(file: UploadFile = File(...)):
    s3_client = S3Client(
        access_key=ACCESS_S3_KEY,
        secret_key=SECRET_S3_KEY,
        endpoint_url=ENDPOINT_URL,
        bucket_name=BUCKET_NAME
    )

    url, content = await s3_client.upload_file(file)
    return JSONResponse({
        "success": True,
        "filename": file.filename,
        "url": url,
        "size": content
    })
