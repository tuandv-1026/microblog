"""Search router."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.api.schemas import PostResponse, SearchResponse
from src.driver.database.connection import get_db
from src.driver.database.repositories import SQLAlchemyPostRepository
from src.usecase.post_usecase import SearchPostsUseCase

router = APIRouter()


@router.get("", response_model=SearchResponse)
async def search_posts(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """Search posts by title or content."""
    post_repo = SQLAlchemyPostRepository(db)
    use_case = SearchPostsUseCase(post_repo)
    
    posts = await use_case.execute(query=q, limit=limit)
    
    return SearchResponse(
        posts=[PostResponse.model_validate(post) for post in posts],
        query=q,
        total=len(posts),
    )
