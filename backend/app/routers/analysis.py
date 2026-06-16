from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.analysis import (
    AnalysisCreateRequest,
    AnalysisResponse,
    AnalysisListResponse,
    AnalysisUpdateRequest
)
from app.services import analysis_service

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/analysis", tags=["analysis"])

import os

@router.post("/", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/hour")
async def create_analysis(
    request: Request,
    obj_in: AnalysisCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new resume analysis.
    """
    if not obj_in.resume_text:
        file_path = os.path.join("data/profiles", f"{current_user.id}.txt")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=400, detail="No resume provided and no saved profile found.")
        with open(file_path, "r", encoding="utf-8") as f:
            obj_in.resume_text = f.read()

    analysis = await analysis_service.create_analysis(db=db, user_id=current_user.id, obj_in=obj_in)
    return analysis

@router.get("/", response_model=AnalysisListResponse)
async def list_analyses(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List all analyses for the current user (paginated).
    """
    items, total = await analysis_service.list_user_analyses(db=db, user_id=current_user.id, page=page, size=size)
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size
    }

@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific analysis by ID.
    """
    analysis = await analysis_service.get_analysis_by_id(db=db, analysis_id=analysis_id, user_id=current_user.id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis

@router.patch("/{analysis_id}", response_model=AnalysisResponse)
async def update_analysis(
    analysis_id: UUID,
    obj_in: AnalysisUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update an analysis (e.g. change the label).
    """
    analysis = await analysis_service.update_analysis_label(
        db=db, analysis_id=analysis_id, user_id=current_user.id, obj_in=obj_in
    )
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis

@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_analysis(
    analysis_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Soft delete an analysis.
    """
    success = await analysis_service.soft_delete_analysis(db=db, analysis_id=analysis_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return None

@router.post("/{analysis_id}/cover-letter")
@limiter.limit("5/hour")
async def generate_cover_letter(
    analysis_id: UUID,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate an AI-powered cover letter based on the analysis resume & job description.
    """
    from app.services import ai_service
    
    analysis = await analysis_service.get_analysis_by_id(db=db, analysis_id=analysis_id, user_id=current_user.id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    cover_letter = await ai_service.generate_cover_letter(
        resume_text=analysis.resume_text,
        job_description=analysis.job_description,
        job_title=analysis.label or ""
    )

    return {"cover_letter": cover_letter}

from pydantic import BaseModel

class JobDescriptionScrapeRequest(BaseModel):
    url: str

@router.post("/scrape-jd")
@limiter.limit("20/hour")
async def scrape_job_description(
    request: Request,
    obj_in: JobDescriptionScrapeRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Scrape and extract job details from a given URL using AI.
    """
    from app.services import ai_service
    
    url_str = obj_in.url.strip()
    if not url_str.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="URL tidak valid. Harus diawali dengan http:// atau https://")
        
    try:
        details = await ai_service.scrape_and_extract_job_details(url_str)
        return {
            "job_title": details.job_title,
            "job_description": details.job_description
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan internal: {str(e)}")
