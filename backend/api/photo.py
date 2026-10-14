from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.schemas.photo import PhotoAnalysisResult
from backend.services.skin_analysis import analyze_image

router = APIRouter(prefix="/api/users/{user_id}", tags=["photo"])
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_BYTES = 8 * 1024 * 1024


@router.post("/skin-photo/analyze", response_model=PhotoAnalysisResult)
async def analyze_skin_photo(user_id: str, photo: UploadFile = File(...)) -> PhotoAnalysisResult:
    if photo.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Use a JPEG, PNG, or WebP image.")
    content = await photo.read(MAX_BYTES + 1)
    if len(content) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="Image must be 8 MB or smaller.")
    return analyze_image(content)
