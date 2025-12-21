import os
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.responses import JSONResponse
from PIL import Image

router = APIRouter(prefix="/uploads", tags=["uploads"])

UPLOAD_DIR = Path(__file__).resolve().parent.parent  / "uploads" / "perfumes"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

print(UPLOAD_DIR)

@router.post('/image')
async def upload_perfume_image(file: UploadFile = File(...)):
    # Создаем каталог, если его еще нет
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    content = await file.read()
    print(content)
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_id = str(uuid.uuid4())
    filename = f"{file_id}{file_ext}"
    filepath = UPLOAD_DIR / filename
    print(filepath)

    with open(filepath, "wb") as buf:
        buf.write(content)

    try:
        optimize_img(filepath)
    except Exception as e:
        print(f"img optimize error: {e}")

    img_url = f"/upload/perfumes/{filename}"

    return JSONResponse({
        "success": True,
        "filename": filename,
        "url": img_url,
        "size": len(content)
    })


def optimize_img(filepath: Path, max_size: tuple = (800, 800)):
    with Image.open(filepath) as img:
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        save_params = {}
        ext = filepath.suffix.lower()
        if ext in {".jpg", ".jpeg"}:
            save_params = {"format": "JPEG", "quality": 85, "optimize": True}
        elif ext == ".webp":
            save_params = {"format": "WEBP", "quality": 85, "method": 6}
        elif ext == ".png":
            save_params = {"format": "PNG", "optimize": True}

        img.save(filepath, **save_params)