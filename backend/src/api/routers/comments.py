"""Comments router."""

from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.api.schemas import CommentCreate, CommentResponse
from src.driver.database.connection import get_db
from src.driver.database.repositories import SQLAlchemyCommentRepository, SQLAlchemyUserRepository
from src.domain.entities import Comment

router = APIRouter()


async def get_current_user_id(session_user_id: Optional[str] = Cookie(None)) -> int:
    """Get current user ID from session cookie."""
    if not session_user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        return int(session_user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid session")


@router.post("", response_model=CommentResponse, status_code=201)
async def create_comment(
    comment_data: CommentCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Create a new comment."""
    comment_repo = SQLAlchemyCommentRepository(db)
    user_repo = SQLAlchemyUserRepository(db)
    
    # Get user info
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    comment = Comment(
        content=comment_data.content,
        author_name=user.username,
        author_email=user.email,
        post_id=comment_data.post_id,
        user_id=user_id,
    )
    
    created_comment = await comment_repo.create(comment)
    return CommentResponse.model_validate(created_comment)


@router.get("/post/{post_id}", response_model=List[CommentResponse])
async def get_post_comments(
    post_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get all comments for a post."""
    comment_repo = SQLAlchemyCommentRepository(db)
    comments = await comment_repo.get_by_post_id(post_id)
    return [CommentResponse.model_validate(comment) for comment in comments]
