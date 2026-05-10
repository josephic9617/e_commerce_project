import os
import uuid

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.core.deps import get_current_admin
from app.core.config import settings
from app.models.user import User

router = APIRouter(prefix="/upload", tags=["Upload"])

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


@router.post("/image")
def upload_image(
    file: UploadFile = File(...),
    admin: User = Depends(get_current_admin),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Faýl ady ýok")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Rugsat edilen formatlar: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        content = file.file.read()
        if len(content) > 5 * 1024 * 1024:  # 5MB limit
            raise HTTPException(status_code=400, detail="Faýl 5MB-den uly")
        f.write(content)

    return {"filename": filename, "url": f"/uploads/{filename}"}
