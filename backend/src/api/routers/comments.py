"""Comments router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.api.schemas import CommentCreate, CommentResponse
from src.driver.database.connection import get_db
from src.driver.database.repositories import SQLAlchemyCommentRepository
from src.domain.entities import Comment

router = APIRouter()


@router.post("", response_model=CommentResponse, status_code=201)
async def create_comment(
    comment_data: CommentCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new comment."""
    comment_repo = SQLAlchemyCommentRepository(db)
    
    comment = Comment(
        content=comment_data.content,
        author_name=comment_data.author_name,
        author_email=comment_data.author_email,
        post_id=comment_data.post_id,
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
