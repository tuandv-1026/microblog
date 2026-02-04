"""Repository interfaces defining data access contracts."""

from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime
from src.domain.entities import User, Post, Category, Comment, Reaction, PostStatus, ReactionType


class UserRepository(ABC):
    """Interface for user data access."""
    
    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user."""
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """Update user."""
        pass


class PostRepository(ABC):
    """Interface for post data access."""
    
    @abstractmethod
    async def create(self, post: Post) -> Post:
        """Create a new post."""
        pass
    
    @abstractmethod
    async def get_by_id(self, post_id: int) -> Optional[Post]:
        """Get post by ID."""
        pass
    
    @abstractmethod
    async def get_by_slug(self, slug: str) -> Optional[Post]:
        """Get post by slug."""
        pass
    
    @abstractmethod
    async def get_all(
        self,
        status: Optional[PostStatus] = None,
        category_id: Optional[int] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> List[Post]:
        """Get all posts with optional filters."""
        pass
    
    @abstractmethod
    async def update(self, post: Post) -> Post:
        """Update post."""
        pass
    
    @abstractmethod
    async def delete(self, post_id: int) -> bool:
        """Delete post."""
        pass
    
    @abstractmethod
    async def search(self, query: str, limit: int = 10) -> List[Post]:
        """Search posts by title or content."""
        pass


class CategoryRepository(ABC):
    """Interface for category data access."""
    
    @abstractmethod
    async def create(self, category: Category) -> Category:
        """Create a new category."""
        pass
    
    @abstractmethod
    async def get_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by ID."""
        pass
    
    @abstractmethod
    async def get_by_slug(self, slug: str) -> Optional[Category]:
        """Get category by slug."""
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Category]:
        """Get all categories."""
        pass
    
    @abstractmethod
    async def get_posts_by_category(self, category_id: int, limit: int = 10) -> List[Post]:
        """Get all posts in a category."""
        pass


class CommentRepository(ABC):
    """Interface for comment data access."""
    
    @abstractmethod
    async def create(self, comment: Comment) -> Comment:
        """Create a new comment."""
        pass
    
    @abstractmethod
    async def get_by_post_id(self, post_id: int) -> List[Comment]:
        """Get all comments for a post."""
        pass
    
    @abstractmethod
    async def delete(self, comment_id: int) -> bool:
        """Delete comment."""
        pass


class ReactionRepository(ABC):
    """Interface for reaction data access."""
    
    @abstractmethod
    async def create(self, reaction: Reaction) -> Reaction:
        """Create a new reaction."""
        pass
    
    @abstractmethod
    async def get_by_post_id(self, post_id: int) -> List[Reaction]:
        """Get all reactions for a post."""
        pass
    
    @abstractmethod
    async def get_user_reaction(self, user_id: int, post_id: int) -> Optional[Reaction]:
        """Get a user's reaction to a post."""
        pass
    
    @abstractmethod
    async def delete(self, reaction_id: int) -> bool:
        """Delete reaction."""
        pass
    
    @abstractmethod
    async def count_by_type(self, post_id: int) -> dict[ReactionType, int]:
        """Count reactions by type for a post."""
        pass
