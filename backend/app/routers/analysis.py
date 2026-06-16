from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.analysis import (
    AnalysisCreateRequest,
    AnalysisResponse,
    AnalysisListResponse,
    AnalysisUpdateRequest
)
from app.services import analysis_service

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.post("/", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def create_analysis(
    obj_in: AnalysisCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new resume analysis.
    """
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
