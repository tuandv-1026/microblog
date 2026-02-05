"""SQLAlchemy implementations of repository interfaces."""

from typing import Optional, List
from sqlalchemy import select, func, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domain.repositories import (
    UserRepository,
    PostRepository,
    CategoryRepository,
    CommentRepository,
    ReactionRepository,
)
from src.domain.entities import User, Post, Category, Comment, Reaction, PostStatus, ReactionType
from src.driver.database.models import (
    UserModel,
    PostModel,
    CategoryModel,
    CommentModel,
    ReactionModel,
    PostStatusEnum,
    ReactionTypeEnum,
)


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy implementation of UserRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, user: User) -> User:
        """Create a new user."""
        db_user = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            bio=user.bio,
        )
        self.session.add(db_user)
        await self.session.flush()
        await self.session.refresh(db_user)
        return self._to_entity(db_user)
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None
    
    async def update(self, user: User) -> User:
        """Update user."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        db_user = result.scalar_one()
        
        db_user.full_name = user.full_name
        db_user.bio = user.bio
        
        await self.session.flush()
        await self.session.refresh(db_user)
        return self._to_entity(db_user)
    
    @staticmethod
    def _to_entity(model: UserModel) -> User:
        """Convert SQLAlchemy model to domain entity."""
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            hashed_password=model.hashed_password,
            full_name=model.full_name,
            bio=model.bio,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class SQLAlchemyPostRepository(PostRepository):
    """SQLAlchemy implementation of PostRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, post: Post) -> Post:
        """Create a new post."""
        db_post = PostModel(
            title=post.title,
            slug=post.slug,
            content_markdown=post.content_markdown,
            content_html=post.content_html,
            excerpt=post.excerpt,
            status=PostStatusEnum(post.status.value),
            author_id=post.author_id,
            published_at=post.published_at,
        )
        self.session.add(db_post)
        await self.session.flush()
        await self.session.refresh(db_post)
        return await self._to_entity(db_post)
    
    async def get_by_id(self, post_id: int) -> Optional[Post]:
        """Get post by ID."""
        result = await self.session.execute(
            select(PostModel)
            .options(selectinload(PostModel.categories))
            .where(PostModel.id == post_id)
        )
        db_post = result.scalar_one_or_none()
        return await self._to_entity(db_post) if db_post else None
    
    async def get_by_slug(self, slug: str) -> Optional[Post]:
        """Get post by slug."""
        result = await self.session.execute(
            select(PostModel)
            .options(selectinload(PostModel.categories))
            .where(PostModel.slug == slug)
        )
        db_post = result.scalar_one_or_none()
        return await self._to_entity(db_post) if db_post else None
    
    async def get_all(
        self,
        status: Optional[PostStatus] = None,
        category_id: Optional[int] = None,
        author_id: Optional[int] = None,
        limit: int = 10,
        offset: int = 0,
        sort_by: str = "newest",
    ) -> List[Post]:
        """Get all posts with optional filters."""
        query = select(PostModel).options(
            selectinload(PostModel.categories),
            selectinload(PostModel.comments),
            selectinload(PostModel.reactions),
        )
        
        if status:
            query = query.where(PostModel.status == PostStatusEnum(status.value))
        
        if category_id:
            query = query.join(PostModel.categories).where(CategoryModel.id == category_id)
        
        if author_id:
            query = query.where(PostModel.author_id == author_id)
        
        # Apply sorting
        if sort_by == "oldest":
            query = query.order_by(PostModel.created_at.asc())
        else:  # newest (default)
            query = query.order_by(PostModel.created_at.desc())
        
        query = query.limit(limit).offset(offset)
        
        result = await self.session.execute(query)
        db_posts = result.scalars().all()
        
        return [await self._to_entity(db_post) for db_post in db_posts]
    
    async def update(self, post: Post) -> Post:
        """Update post."""
        result = await self.session.execute(
            select(PostModel).where(PostModel.id == post.id)
        )
        db_post = result.scalar_one()
        
        db_post.title = post.title
        db_post.content_markdown = post.content_markdown
        db_post.content_html = post.content_html
        db_post.excerpt = post.excerpt
        db_post.status = PostStatusEnum(post.status.value)
        db_post.view_count = post.view_count
        db_post.published_at = post.published_at
        
        await self.session.flush()
        await self.session.refresh(db_post)
        return await self._to_entity(db_post)
    
    async def delete(self, post_id: int) -> bool:
        """Delete post."""
        result = await self.session.execute(
            delete(PostModel).where(PostModel.id == post_id)
        )
        return result.rowcount > 0
    
    async def search(self, query: str, limit: int = 10) -> List[Post]:
        """Search posts by title or content."""
        search_pattern = f"%{query}%"
        result = await self.session.execute(
            select(PostModel)
            .options(selectinload(PostModel.categories))
            .where(
                or_(
                    PostModel.title.like(search_pattern),
                    PostModel.content_markdown.like(search_pattern),
                )
            )
            .where(PostModel.status == PostStatusEnum.PUBLISHED)
            .order_by(PostModel.created_at.desc())
            .limit(limit)
        )
        db_posts = result.scalars().all()
        return [await self._to_entity(db_post) for db_post in db_posts]
    
    async def _to_entity(self, model: PostModel) -> Post:
        """Convert SQLAlchemy model to domain entity."""
        # Load relationships if not already loaded
        await self.session.refresh(model, ['categories', 'comments', 'reactions'])
        
        return Post(
            id=model.id,
            title=model.title,
            slug=model.slug,
            content_markdown=model.content_markdown,
            content_html=model.content_html,
            excerpt=model.excerpt,
            status=PostStatus(model.status.value),
            author_id=model.author_id,
            view_count=model.view_count,
            published_at=model.published_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
            categories=[
                Category(
                    id=cat.id,
                    name=cat.name,
                    slug=cat.slug,
                    description=cat.description,
                    created_at=cat.created_at,
                )
                for cat in model.categories
            ],
            comments=[
                Comment(
                    id=comment.id,
                    content=comment.content,
                    author_name=comment.author_name,
                    author_email=comment.author_email,
                    post_id=comment.post_id,
                    created_at=comment.created_at,
                )
                for comment in model.comments
            ],
            reactions=[
                Reaction(
                    id=reaction.id,
                    type=ReactionType(reaction.type.value),
                    user_id=reaction.user_id,
                    post_id=reaction.post_id,
                    created_at=reaction.created_at,
                )
                for reaction in model.reactions
            ],
        )


class SQLAlchemyCategoryRepository(CategoryRepository):
    """SQLAlchemy implementation of CategoryRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, category: Category) -> Category:
        """Create a new category."""
        db_category = CategoryModel(
            name=category.name,
            slug=category.slug,
            description=category.description,
        )
        self.session.add(db_category)
        await self.session.flush()
        await self.session.refresh(db_category)
        return self._to_entity(db_category)
    
    async def get_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by ID."""
        result = await self.session.execute(
            select(CategoryModel).where(CategoryModel.id == category_id)
        )
        db_category = result.scalar_one_or_none()
        return self._to_entity(db_category) if db_category else None
    
    async def get_by_slug(self, slug: str) -> Optional[Category]:
        """Get category by slug."""
        result = await self.session.execute(
            select(CategoryModel).where(CategoryModel.slug == slug)
        )
        db_category = result.scalar_one_or_none()
        return self._to_entity(db_category) if db_category else None
    
    async def get_all(self) -> List[Category]:
        """Get all categories."""
        result = await self.session.execute(
            select(CategoryModel).order_by(CategoryModel.name)
        )
        db_categories = result.scalars().all()
        return [self._to_entity(cat) for cat in db_categories]
    
    async def get_posts_by_category(self, category_id: int, limit: int = 10) -> List[Post]:
        """Get all posts in a category."""
        result = await self.session.execute(
            select(PostModel)
            .join(PostModel.categories)
            .where(CategoryModel.id == category_id)
            .where(PostModel.status == PostStatusEnum.PUBLISHED)
            .order_by(PostModel.published_at.desc())
            .limit(limit)
        )
        db_posts = result.scalars().all()
        
        # Convert to entities using PostRepository logic
        from src.driver.database.repositories import SQLAlchemyPostRepository
        post_repo = SQLAlchemyPostRepository(self.session)
        return [await post_repo._to_entity(db_post) for db_post in db_posts]
    
    @staticmethod
    def _to_entity(model: CategoryModel) -> Category:
        """Convert SQLAlchemy model to domain entity."""
        return Category(
            id=model.id,
            name=model.name,
            slug=model.slug,
            description=model.description,
            created_at=model.created_at,
        )


class SQLAlchemyCommentRepository(CommentRepository):
    """SQLAlchemy implementation of CommentRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, comment: Comment) -> Comment:
        """Create a new comment."""
        db_comment = CommentModel(
            content=comment.content,
            author_name=comment.author_name,
            author_email=comment.author_email,
            post_id=comment.post_id,
            user_id=comment.user_id,
        )
        self.session.add(db_comment)
        await self.session.flush()
        await self.session.refresh(db_comment)
        return self._to_entity(db_comment)
    
    async def get_by_post_id(self, post_id: int) -> List[Comment]:
        """Get all comments for a post."""
        result = await self.session.execute(
            select(CommentModel)
            .where(CommentModel.post_id == post_id)
            .order_by(CommentModel.created_at.desc())
        )
        db_comments = result.scalars().all()
        return [self._to_entity(comment) for comment in db_comments]
    
    async def delete(self, comment_id: int) -> bool:
        """Delete comment."""
        result = await self.session.execute(
            delete(CommentModel).where(CommentModel.id == comment_id)
        )
        return result.rowcount > 0
    
    @staticmethod
    def _to_entity(model: CommentModel) -> Comment:
        """Convert SQLAlchemy model to domain entity."""
        return Comment(
            id=model.id,
            content=model.content,
            author_name=model.author_name,
            author_email=model.author_email,
            post_id=model.post_id,
            user_id=model.user_id,
            created_at=model.created_at,
        )


class SQLAlchemyReactionRepository(ReactionRepository):
    """SQLAlchemy implementation of ReactionRepository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, reaction: Reaction) -> Reaction:
        """Create a new reaction."""
        db_reaction = ReactionModel(
            type=ReactionTypeEnum(reaction.type.value),
            user_id=reaction.user_id,
            post_id=reaction.post_id,
        )
        self.session.add(db_reaction)
        await self.session.flush()
        await self.session.refresh(db_reaction)
        return self._to_entity(db_reaction)
    
    async def get_by_post_id(self, post_id: int) -> List[Reaction]:
        """Get all reactions for a post."""
        result = await self.session.execute(
            select(ReactionModel).where(ReactionModel.post_id == post_id)
        )
        db_reactions = result.scalars().all()
        return [self._to_entity(reaction) for reaction in db_reactions]
    
    async def get_user_reaction(self, user_id: int, post_id: int) -> Optional[Reaction]:
        """Get a user's reaction to a post."""
        result = await self.session.execute(
            select(ReactionModel)
            .where(ReactionModel.user_id == user_id)
            .where(ReactionModel.post_id == post_id)
        )
        db_reaction = result.scalar_one_or_none()
        return self._to_entity(db_reaction) if db_reaction else None
    
    async def delete(self, reaction_id: int) -> bool:
        """Delete reaction."""
        result = await self.session.execute(
            delete(ReactionModel).where(ReactionModel.id == reaction_id)
        )
        return result.rowcount > 0
    
    async def count_by_type(self, post_id: int) -> dict[ReactionType, int]:
        """Count reactions by type for a post."""
        result = await self.session.execute(
            select(ReactionModel.type, func.count(ReactionModel.id))
            .where(ReactionModel.post_id == post_id)
            .group_by(ReactionModel.type)
        )
        
        counts = {reaction_type: 0 for reaction_type in ReactionType}
        for db_type, count in result:
            counts[ReactionType(db_type.value)] = count
        
        return counts
    
    @staticmethod
    def _to_entity(model: ReactionModel) -> Reaction:
        """Convert SQLAlchemy model to domain entity."""
        return Reaction(
            id=model.id,
            type=ReactionType(model.type.value),
            user_id=model.user_id,
            post_id=model.post_id,
            created_at=model.created_at,
        )
