"""Reactions router."""

from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.api.schemas import ReactionCreate, ReactionResponse, ReactionSummary
from src.driver.database.connection import get_db
from src.driver.database.repositories import SQLAlchemyReactionRepository
from src.domain.entities import Reaction, ReactionType

router = APIRouter()


async def get_current_user_id(session_user_id: Optional[str] = Cookie(None)) -> int:
    """Dependency to get current user ID from session."""
    if not session_user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        return int(session_user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid session")


@router.post("", response_model=ReactionResponse, status_code=201)
async def toggle_reaction(
    reaction_data: ReactionCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Toggle a reaction on a post."""
    reaction_repo = SQLAlchemyReactionRepository(db)
    
    # Check if user already reacted to this post
    existing_reaction = await reaction_repo.get_user_reaction(user_id, reaction_data.post_id)
    
    if existing_reaction:
        # If same type, remove reaction
        if existing_reaction.type == reaction_data.type:
            await reaction_repo.delete(existing_reaction.id)
            raise HTTPException(status_code=204, detail="Reaction removed")
        else:
            # If different type, delete old and create new
            await reaction_repo.delete(existing_reaction.id)
    
    # Create new reaction
    reaction = Reaction(
        type=reaction_data.type,
        user_id=user_id,
        post_id=reaction_data.post_id,
    )
    
    created_reaction = await reaction_repo.create(reaction)
    return ReactionResponse.model_validate(created_reaction)


@router.get("/post/{post_id}/summary", response_model=ReactionSummary)
async def get_post_reactions_summary(
    post_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get reaction counts for a post."""
    reaction_repo = SQLAlchemyReactionRepository(db)
    counts = await reaction_repo.count_by_type(post_id)
    
    total = sum(counts.values())
    
    return ReactionSummary(
        like=counts.get(ReactionType.LIKE, 0),
        love=counts.get(ReactionType.LOVE, 0),
        haha=counts.get(ReactionType.HAHA, 0),
        wow=counts.get(ReactionType.WOW, 0),
        sad=counts.get(ReactionType.SAD, 0),
        angry=counts.get(ReactionType.ANGRY, 0),
        total=total,
    )
