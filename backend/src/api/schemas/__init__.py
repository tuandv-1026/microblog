"""Pydantic schemas for API request/response validation."""

from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
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


# User Schemas
class UserBase(BaseModel):
    """Base user schema."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str = Field(..., min_length=8, max_length=100)
    full_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    full_name: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Auth Schemas
class LoginRequest(BaseModel):
    """Schema for login request."""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Schema for login response."""
    user: UserResponse
    message: str = "Login successful"


# Category Schemas
class CategoryBase(BaseModel):
    """Base category schema."""
    name: str = Field(..., min_length=1, max_length=50)
    slug: str = Field(..., min_length=1, max_length=60)
    description: Optional[str] = Field(None, max_length=255)


class CategoryCreate(CategoryBase):
    """Schema for creating a category."""
    pass


class CategoryResponse(CategoryBase):
    """Schema for category response."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Post Schemas
class PostBase(BaseModel):
    """Base post schema."""
    title: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=250)
    content_markdown: str = Field(..., min_length=1)


class PostCreate(PostBase):
    """Schema for creating a post."""
    excerpt: Optional[str] = Field(None, max_length=500)
    category_ids: Optional[List[int]] = []


class PostUpdate(BaseModel):
    """Schema for updating a post."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content_markdown: Optional[str] = Field(None, min_length=1)
    excerpt: Optional[str] = Field(None, max_length=500)
    category_ids: Optional[List[int]] = None


class PostResponse(PostBase):
    """Schema for post response."""
    id: int
    content_html: str
    excerpt: Optional[str] = None
    status: PostStatus
    author_id: int
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    categories: List[CategoryResponse] = []
    
    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    """Schema for paginated post list."""
    posts: List[PostResponse]
    total: int
    limit: int
    offset: int


# Comment Schemas
class CommentBase(BaseModel):
    """Base comment schema."""
    content: str = Field(..., min_length=1, max_length=1000)
    author_name: str = Field(..., min_length=1, max_length=100)
    author_email: EmailStr


class CommentCreate(CommentBase):
    """Schema for creating a comment."""
    post_id: int


class CommentResponse(CommentBase):
    """Schema for comment response."""
    id: int
    post_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Reaction Schemas
class ReactionCreate(BaseModel):
    """Schema for creating a reaction."""
    type: ReactionType
    post_id: int


class ReactionResponse(BaseModel):
    """Schema for reaction response."""
    id: int
    type: ReactionType
    user_id: int
    post_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ReactionSummary(BaseModel):
    """Schema for reaction count summary."""
    like: int = 0
    love: int = 0
    haha: int = 0
    wow: int = 0
    sad: int = 0
    angry: int = 0
    total: int = 0


# Search Schema
class SearchResponse(BaseModel):
    """Schema for search results."""
    posts: List[PostResponse]
    query: str
    total: int


# About Schema
class AboutResponse(BaseModel):
    """Schema for about page response."""
    title: str = "About This Blog"
    content_html: str
    author: UserResponse
