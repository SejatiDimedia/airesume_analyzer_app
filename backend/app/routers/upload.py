from fastapi import APIRouter, Depends, UploadFile, File
from app.dependencies import get_current_user
from app.models.user import User
from app.services.file_service import extract_text

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/test-parse")
async def test_parse_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Test endpoint for extracting text from a PDF or DOCX resume.
    Requires an authenticated user.
    """
    text = await extract_text(file)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "extracted_text": text
    }
