"""About router."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import AboutResponse, UserResponse
from src.driver.database.connection import get_db
from src.driver.database.repositories import SQLAlchemyUserRepository
from src.service.markdown_service import markdown_service

router = APIRouter()

# Static about content (can be stored in database or config)
ABOUT_MARKDOWN = """
# About This Blog

Welcome to my personal microblog! This is a simple platform for sharing my thoughts, 
ideas, and experiences through Markdown-formatted posts.

## Features

- **Markdown Support**: Write posts in Markdown with syntax highlighting
- **Categories**: Organize posts by categories
- **Comments**: Engage with readers through comments
- **Reactions**: Express emotions with emoji reactions
- **Search**: Find posts quickly with full-text search

## Technology

Built with modern web technologies:
- FastAPI for the backend API
- React for the frontend
- MySQL for data persistence
- Docker for containerization

## Contact

Feel free to reach out through the comment section on any post!
"""


@router.get("", response_model=AboutResponse)
async def get_about(
    db: AsyncSession = Depends(get_db),
):
    """Get about page content."""
    # Get the first user (blog author)
    user_repo = SQLAlchemyUserRepository(db)
    author = await user_repo.get_by_id(1)  # Assuming first user is the author
    
    if not author:
        # Return default if no author found
        return AboutResponse(
            title="About This Blog",
            content_html=markdown_service.render(ABOUT_MARKDOWN),
            author=UserResponse(
                id=0,
                username="admin",
                email="admin@example.com",
                full_name="Blog Administrator",
                created_at="2024-01-01T00:00:00",
            ),
        )
    
    return AboutResponse(
        title="About This Blog",
        content_html=markdown_service.render(ABOUT_MARKDOWN),
        author=UserResponse.model_validate(author),
    )
