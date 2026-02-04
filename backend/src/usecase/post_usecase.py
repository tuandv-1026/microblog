"""Use cases for post operations."""

from typing import Optional, List
from datetime import datetime
from src.domain.entities import Post, PostStatus
from src.domain.repositories import PostRepository, CategoryRepository
from src.service.markdown_service import markdown_service


class CreatePostUseCase:
    """Use case for creating a post."""
    
    def __init__(self, post_repository: PostRepository, category_repository: CategoryRepository):
        self.post_repository = post_repository
        self.category_repository = category_repository
    
    async def execute(
        self,
        title: str,
        slug: str,
        content_markdown: str,
        author_id: int,
        excerpt: Optional[str] = None,
        category_ids: Optional[List[int]] = None,
    ) -> Post:
        """
        Create a new post.
        
        Raises:
            ValueError: If slug already exists
        """
        # Check if slug exists
        existing_post = await self.post_repository.get_by_slug(slug)
        if existing_post:
            raise ValueError("Slug already exists")
        
        # Render Markdown to HTML
        content_html = markdown_service.render(content_markdown)
        
        # Generate excerpt if not provided
        if not excerpt:
            excerpt = markdown_service.generate_excerpt(content_markdown)
        
        # Create post entity
        post = Post(
            title=title,
            slug=slug,
            content_markdown=content_markdown,
            content_html=content_html,
            excerpt=excerpt,
            status=PostStatus.DRAFT,
            author_id=author_id,
        )
        
        # Save to database
        created_post = await self.post_repository.create(post)
        
        return created_post


class UpdatePostUseCase:
    """Use case for updating a post."""
    
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository
    
    async def execute(
        self,
        post_id: int,
        title: Optional[str] = None,
        content_markdown: Optional[str] = None,
        excerpt: Optional[str] = None,
    ) -> Post:
        """
        Update an existing post.
        
        Raises:
            ValueError: If post not found
        """
        # Get existing post
        post = await self.post_repository.get_by_id(post_id)
        if not post:
            raise ValueError("Post not found")
        
        # Update fields
        if title:
            post.title = title
        
        if content_markdown:
            post.content_markdown = content_markdown
            post.content_html = markdown_service.render(content_markdown)
            
            if not excerpt:
                post.excerpt = markdown_service.generate_excerpt(content_markdown)
        
        if excerpt:
            post.excerpt = excerpt
        
        # Save changes
        return await self.post_repository.update(post)


class PublishPostUseCase:
    """Use case for publishing a post."""
    
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository
    
    async def execute(self, post_id: int) -> Post:
        """
        Publish a draft post.
        
        Raises:
            ValueError: If post not found or already published
        """
        # Get post
        post = await self.post_repository.get_by_id(post_id)
        if not post:
            raise ValueError("Post not found")
        
        if post.status == PostStatus.PUBLISHED:
            raise ValueError("Post is already published")
        
        # Update status
        post.status = PostStatus.PUBLISHED
        post.published_at = datetime.utcnow()
        
        return await self.post_repository.update(post)


class GetPostsUseCase:
    """Use case for retrieving posts."""
    
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository
    
    async def execute(
        self,
        status: Optional[PostStatus] = None,
        category_id: Optional[int] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> List[Post]:
        """Get posts with optional filters."""
        return await self.post_repository.get_all(
            status=status,
            category_id=category_id,
            limit=limit,
            offset=offset,
        )


class SearchPostsUseCase:
    """Use case for searching posts."""
    
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository
    
    async def execute(self, query: str, limit: int = 10) -> List[Post]:
        """Search posts by title or content."""
        return await self.post_repository.search(query, limit)


class DeletePostUseCase:
    """Use case for deleting a post."""
    
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository
    
    async def execute(self, post_id: int) -> bool:
        """Delete a post."""
        return await self.post_repository.delete(post_id)
