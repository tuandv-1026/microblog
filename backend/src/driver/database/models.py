"""SQLAlchemy models for database tables."""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from src.driver.database.connection import Base
import enum


class PostStatusEnum(str, enum.Enum):
    """Post publication status."""
    DRAFT = "draft"
    PUBLISHED = "published"


class ReactionTypeEnum(str, enum.Enum):
    """Types of reactions."""
    LIKE = "like"
    LOVE = "love"
    HAHA = "haha"
    WOW = "wow"
    SAD = "sad"
    ANGRY = "angry"


# Association table for Post-Category many-to-many relationship
post_categories = Table(
    'post_categories',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True),
    Index('idx_post_categories_post', 'post_id'),
    Index('idx_post_categories_category', 'category_id'),
)


class UserModel(Base):
    """User table model."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    posts = relationship("PostModel", back_populates="author", cascade="all, delete-orphan")
    reactions = relationship("ReactionModel", back_populates="user", cascade="all, delete-orphan")


class PostModel(Base):
    """Post table model."""
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, index=True)
    slug = Column(String(250), unique=True, nullable=False, index=True)
    content_markdown = Column(Text, nullable=False)
    content_html = Column(Text, nullable=False)
    excerpt = Column(String(500), nullable=True)
    status = Column(SQLEnum(PostStatusEnum), default=PostStatusEnum.DRAFT, nullable=False, index=True)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    view_count = Column(Integer, default=0, nullable=False)
    published_at = Column(DateTime, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    author = relationship("UserModel", back_populates="posts")
    categories = relationship("CategoryModel", secondary=post_categories, back_populates="posts")
    comments = relationship("CommentModel", back_populates="post", cascade="all, delete-orphan")
    reactions = relationship("ReactionModel", back_populates="post", cascade="all, delete-orphan")
    
    # Composite indexes
    __table_args__ = (
        Index('idx_posts_status_published', 'status', 'published_at'),
        Index('idx_posts_author_status', 'author_id', 'status'),
    )


class CategoryModel(Base):
    """Category table model."""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    slug = Column(String(60), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    posts = relationship("PostModel", secondary=post_categories, back_populates="categories")


class CommentModel(Base):
    """Comment table model."""
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    author_name = Column(String(100), nullable=False)
    author_email = Column(String(255), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    post = relationship("PostModel", back_populates="comments")


class ReactionModel(Base):
    """Reaction table model."""
    __tablename__ = 'reactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(SQLEnum(ReactionTypeEnum), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("UserModel", back_populates="reactions")
    post = relationship("PostModel", back_populates="reactions")
    
    # Composite indexes and constraints
    __table_args__ = (
        Index('idx_reactions_user_post', 'user_id', 'post_id', unique=True),
        Index('idx_reactions_post_type', 'post_id', 'type'),
    )
