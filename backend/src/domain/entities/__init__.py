"""Domain entities for the microblog application."""

from datetime import datetime
from typing import Optional, List
from enum import Enum


class PostStatus(str, Enum):
    """Post publication status."""
    DRAFT = "draft"
    PUBLISHED = "published"


class ReactionType(str, Enum):
    """Types of reactions."""
    LIKE = "like"
    LOVE = "love"
    HAHA = "haha"
    WOW = "wow"
    SAD = "sad"
    ANGRY = "angry"


class User:
    """User domain entity."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        username: str = "",
        email: str = "",
        hashed_password: str = "",
        full_name: Optional[str] = None,
        bio: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.full_name = full_name
        self.bio = bio
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()


class Post:
    """Post domain entity."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        title: str = "",
        slug: str = "",
        content_markdown: str = "",
        content_html: str = "",
        excerpt: Optional[str] = None,
        status: PostStatus = PostStatus.DRAFT,
        author_id: Optional[int] = None,
        view_count: int = 0,
        published_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        categories: Optional[List['Category']] = None,
        comments: Optional[List['Comment']] = None,
        reactions: Optional[List['Reaction']] = None,
    ):
        self.id = id
        self.title = title
        self.slug = slug
        self.content_markdown = content_markdown
        self.content_html = content_html
        self.excerpt = excerpt
        self.status = status
        self.author_id = author_id
        self.view_count = view_count
        self.published_at = published_at
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.categories = categories or []
        self.comments = comments or []
        self.reactions = reactions or []


class Category:
    """Category domain entity."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        name: str = "",
        slug: str = "",
        description: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.name = name
        self.slug = slug
        self.description = description
        self.created_at = created_at or datetime.utcnow()


class Comment:
    """Comment domain entity."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        content: str = "",
        author_name: str = "",
        author_email: str = "",
        post_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.content = content
        self.author_name = author_name
        self.author_email = author_email
        self.post_id = post_id
        self.created_at = created_at or datetime.utcnow()


class Reaction:
    """Reaction domain entity."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        type: ReactionType = ReactionType.LIKE,
        user_id: Optional[int] = None,
        post_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.type = type
        self.user_id = user_id
        self.post_id = post_id
        self.created_at = created_at or datetime.utcnow()
