"""Categories router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.api.schemas import CategoryResponse
from src.driver.database.connection import get_db
from src.driver.database.repositories import SQLAlchemyCategoryRepository

router = APIRouter()


@router.get("", response_model=List[CategoryResponse])
async def get_categories(
    db: AsyncSession = Depends(get_db),
):
    """Get all categories."""
    category_repo = SQLAlchemyCategoryRepository(db)
    categories = await category_repo.get_all()
    return [CategoryResponse.model_validate(cat) for cat in categories]


@router.get("/{slug}", response_model=CategoryResponse)
async def get_category(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """Get a category by slug."""
    category_repo = SQLAlchemyCategoryRepository(db)
    category = await category_repo.get_by_slug(slug)
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return CategoryResponse.model_validate(category)
