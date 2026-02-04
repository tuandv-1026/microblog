"""Posts router for CRUD operations."""

from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from src.api.schemas import PostCreate, PostUpdate, PostResponse, PostListResponse
from src.driver.database.connection import get_db
from src.driver.database.repositories import SQLAlchemyPostRepository, SQLAlchemyCategoryRepository
from src.usecase.post_usecase import (
    CreatePostUseCase,
    UpdatePostUseCase,
    PublishPostUseCase,
    GetPostsUseCase,
    DeletePostUseCase,
)
from src.domain.entities import PostStatus

router = APIRouter()


async def get_current_user_id(session_user_id: Optional[str] = Cookie(None)) -> int:
    """Dependency to get current user ID from session."""
    if not session_user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        return int(session_user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid session")


@router.post("", response_model=PostResponse, status_code=201)
async def create_post(
    post_data: PostCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Create a new post (draft)."""
    post_repo = SQLAlchemyPostRepository(db)
    category_repo = SQLAlchemyCategoryRepository(db)
    use_case = CreatePostUseCase(post_repo, category_repo)
    
    try:
        post = await use_case.execute(
            title=post_data.title,
            slug=post_data.slug,
            content_markdown=post_data.content_markdown,
            author_id=user_id,
            excerpt=post_data.excerpt,
            category_ids=post_data.category_ids,
        )
        return PostResponse.model_validate(post)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[PostResponse])
async def get_posts(
    status: Optional[str] = None,
    category_id: Optional[int] = None,
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """Get all posts with optional filters."""
    post_repo = SQLAlchemyPostRepository(db)
    use_case = GetPostsUseCase(post_repo)
    
    post_status = PostStatus(status) if status else None
    posts = await use_case.execute(
        status=post_status,
        category_id=category_id,
        limit=limit,
        offset=offset,
    )
    
    return [PostResponse.model_validate(post) for post in posts]


@router.get("/{slug}", response_model=PostResponse)
async def get_post(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """Get a post by slug."""
    post_repo = SQLAlchemyPostRepository(db)
    post = await post_repo.get_by_slug(slug)
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return PostResponse.model_validate(post)


@router.patch("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Update a post."""
    post_repo = SQLAlchemyPostRepository(db)
    
    # Verify ownership
    post = await post_repo.get_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    use_case = UpdatePostUseCase(post_repo)
    
    try:
        updated_post = await use_case.execute(
            post_id=post_id,
            title=post_data.title,
            content_markdown=post_data.content_markdown,
            excerpt=post_data.excerpt,
        )
        return PostResponse.model_validate(updated_post)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{post_id}/publish", response_model=PostResponse)
async def publish_post(
    post_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Publish a draft post."""
    post_repo = SQLAlchemyPostRepository(db)
    
    # Verify ownership
    post = await post_repo.get_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    use_case = PublishPostUseCase(post_repo)
    
    try:
        published_post = await use_case.execute(post_id=post_id)
        return PostResponse.model_validate(published_post)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{post_id}", status_code=204)
async def delete_post(
    post_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Delete a post."""
    post_repo = SQLAlchemyPostRepository(db)
    
    # Verify ownership
    post = await post_repo.get_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    use_case = DeletePostUseCase(post_repo)
    deleted = await use_case.execute(post_id=post_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found")
