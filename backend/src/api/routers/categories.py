"""Categories router."""

from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.api.schemas import CategoryResponse, CategoryCreate
from src.driver.database.connection import get_db
from src.driver.database.repositories import SQLAlchemyCategoryRepository
from src.domain.entities import Category

router = APIRouter()


async def get_current_user_id(session_user_id: Optional[str] = Cookie(None)) -> int:
    """Get current user ID from session cookie."""
    if not session_user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        return int(session_user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid session")


@router.post("", response_model=CategoryResponse, status_code=201)
async def create_category(
    category_data: CategoryCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Create a new category."""
    category_repo = SQLAlchemyCategoryRepository(db)
    
    # Check if category with same slug already exists
    existing = await category_repo.get_by_slug(category_data.slug)
    if existing:
        raise HTTPException(status_code=400, detail="Category with this slug already exists")
    
    category = Category(
        name=category_data.name,
        slug=category_data.slug,
        description=category_data.description,
    )
    
    created_category = await category_repo.create(category)
    return CategoryResponse.model_validate(created_category)


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
