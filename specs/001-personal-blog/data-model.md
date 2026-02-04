# Data Model: Personal Blog Platform

**Date**: 2026-02-04  
**Phase**: 1 - Design & Contracts  
**Source**: Derived from [spec.md](spec.md) functional requirements and [research.md](research.md) technical decisions

## Entity Relationship Diagram

```
┌─────────────────────┐
│       User          │
├─────────────────────┤
│ id (PK)             │
│ email (unique)      │
│ username (unique)   │
│ hashed_password     │
│ created_at          │
│ role                │
└─────────────────────┘
         │ 1
         │ authored_by
         │
         │ *
┌─────────────────────┐                    ┌─────────────────────┐
│       Post          │ * ─────────── * │      Category       │
├─────────────────────┤   post_categories   ├─────────────────────┤
│ id (PK)             │                    │ id (PK)             │
│ title               │                    │ name (unique)       │
│ content (Markdown)  │                    │ slug (unique)       │
│ author_id (FK)      │                    │ created_at          │
│ status              │                    └─────────────────────┘
│ view_count          │
│ created_at          │
│ published_at        │
│ updated_at          │
└─────────────────────┘
         │ 1
         ├───────────────┐
         │               │
         │ *             │ *
┌─────────────────────┐ ┌─────────────────────┐
│      Comment        │ │      Reaction       │
├─────────────────────┤ ├─────────────────────┤
│ id (PK)             │ │ id (PK)             │
│ post_id (FK)        │ │ post_id (FK)        │
│ user_id (FK)        │ │ user_id (FK)        │
│ content             │ │ type                │
│ created_at          │ │ created_at          │
└─────────────────────┘ └─────────────────────┘
         │ *                     │ *
         │                       │
         │ 1                     │ 1
         └───────────────────────┘
                 User
```

## Entities

### User

Represents a registered account with authentication credentials and authoring capabilities.

**Attributes**:
- `id` (Integer, Primary Key): Auto-incrementing unique identifier
- `email` (String(255), Unique, Not Null): User email address for login (validated via Pydantic)
- `username` (String(50), Unique, Not Null): Display name for posts and comments
- `hashed_password` (String(255), Not Null): bcrypt-hashed password (cost factor 12)
- `role` (Enum: 'author', 'admin', Not Null, Default: 'author'): User permission level
- `created_at` (DateTime, Not Null, Default: now()): Account registration timestamp

**Relationships**:
- `posts` (One-to-Many → Post): Posts authored by this user
- `comments` (One-to-Many → Comment): Comments created by this user
- `reactions` (One-to-Many → Reaction): Emoji reactions by this user

**Validation Rules**:
- Email format: RFC 5322 compliant (validated in API layer via Pydantic)
- Username: 3-50 characters, alphanumeric + underscore/hyphen
- Password (pre-hash): Minimum 8 characters (validated before hashing)

**Indexes**:
- `idx_user_email` on `email` (unique, for login queries)
- `idx_user_username` on `username` (unique, for display and search)

**State Transitions**: None (immutable role after creation in v1)

---

### Post

Represents a blog post with Markdown content, categories, and engagement metrics.

**Attributes**:
- `id` (Integer, Primary Key): Auto-incrementing unique identifier
- `title` (String(255), Not Null): Post title (displayed in previews and detail page)
- `content` (Text, Not Null): Raw Markdown content (stored as plaintext)
- `author_id` (Integer, Foreign Key → User.id, Not Null): Author who created the post
- `status` (Enum: 'draft', 'published', Not Null, Default: 'draft'): Publication state
- `view_count` (Integer, Not Null, Default: 0): Number of unique views (session-based tracking)
- `created_at` (DateTime, Not Null, Default: now()): Post creation timestamp
- `published_at` (DateTime, Nullable): Timestamp when post was first published (null for drafts)
- `updated_at` (DateTime, Not Null, Default: now(), onupdate=now()): Last modification timestamp

**Relationships**:
- `author` (Many-to-One → User): User who authored the post
- `categories` (Many-to-Many → Category via `post_categories`): Tags assigned to post
- `comments` (One-to-Many → Comment): Comments on this post
- `reactions` (One-to-Many → Reaction): Emoji reactions to this post

**Validation Rules**:
- Title: Non-empty, max 255 characters
- Content: Non-empty (validated before publish; drafts allow empty content)
- Status: Can only transition draft → published (no unpublishing in v1)
- Published_at: Automatically set when status changes to 'published' (never updated after)

**Indexes**:
- `idx_post_status_created` on `(status, created_at DESC)` (for homepage sorting by newest published)
- `idx_post_author` on `author_id` (for author's post list)
- `idx_post_published_at` on `published_at` (for timeline queries)

**State Transitions**:
```
[draft] ──(publish)──> [published]
  │
  └──(delete)──> [removed]
```

**Computed Fields** (not stored, calculated at query time):
- `like_count`: Count of reactions where `type = 'like'`
- `excerpt`: First 150 characters of `content` (Markdown stripped for preview)

---

### Category

Represents a tag or category for organizing posts.

**Attributes**:
- `id` (Integer, Primary Key): Auto-incrementing unique identifier
- `name` (String(50), Unique, Not Null): Human-readable category name (e.g., "Technology")
- `slug` (String(50), Unique, Not Null): URL-friendly identifier (e.g., "technology")
- `created_at` (DateTime, Not Null, Default: now()): Category creation timestamp

**Relationships**:
- `posts` (Many-to-Many → Post via `post_categories`): Posts tagged with this category

**Validation Rules**:
- Name: Non-empty, max 50 characters, unique
- Slug: Auto-generated from name (lowercase, spaces → hyphens), unique

**Indexes**:
- `idx_category_slug` on `slug` (unique, for category page URLs)

**Computed Fields**:
- `post_count`: Count of published posts in this category (for sidebar display)

---

### Comment

Represents a user comment on a published post.

**Attributes**:
- `id` (Integer, Primary Key): Auto-incrementing unique identifier
- `post_id` (Integer, Foreign Key → Post.id, Not Null): Post being commented on
- `user_id` (Integer, Foreign Key → User.id, Not Null): User who created the comment
- `content` (Text, Not Null): Comment text (plaintext, no Markdown in v1)
- `created_at` (DateTime, Not Null, Default: now()): Comment creation timestamp

**Relationships**:
- `post` (Many-to-One → Post): Post this comment belongs to
- `user` (Many-to-One → User): User who authored the comment

**Validation Rules**:
- Content: Non-empty, max 1000 characters (to prevent spam)
- Post must be published (drafts cannot be commented on)
- User must be authenticated

**Indexes**:
- `idx_comment_post_created` on `(post_id, created_at ASC)` (for chronological ordering)
- `idx_comment_user` on `user_id` (for user's comment history)

**State Transitions**: None (comments are immutable in v1; delete is only action)

---

### Reaction

Represents an emoji reaction to a post (like, haha, angry, sad).

**Attributes**:
- `id` (Integer, Primary Key): Auto-incrementing unique identifier
- `post_id` (Integer, Foreign Key → Post.id, Not Null): Post being reacted to
- `user_id` (Integer, Foreign Key → User.id, Not Null): User who reacted
- `type` (Enum: 'like', 'haha', 'angry', 'sad', Not Null): Emoji type
- `created_at` (DateTime, Not Null, Default: now()): Reaction timestamp

**Relationships**:
- `post` (Many-to-One → Post): Post this reaction belongs to
- `user` (Many-to-One → User): User who created the reaction

**Validation Rules**:
- One reaction per user per type per post (unique constraint on `(post_id, user_id, type)`)
- User must be authenticated
- Post must be published

**Indexes**:
- `idx_reaction_post_type` on `(post_id, type)` (for aggregating reaction counts)
- `unique_reaction` on `(post_id, user_id, type)` (unique constraint)

**State Transitions**:
```
[none] ──(react)──> [active] ──(unreact)──> [removed]
```
(Toggle behavior: clicking same emoji removes reaction)

---

### AboutPage (Optional Entity)

Represents the About Me page content (alternative: single row in settings table).

**Attributes**:
- `id` (Integer, Primary Key): Single row (id=1)
- `content` (Text, Not Null): About page content in Markdown
- `profile_photo_url` (String(500), Nullable): URL to profile photo (external or uploaded)
- `updated_at` (DateTime, Not Null, Default: now(), onupdate=now()): Last edit timestamp

**Relationships**: None

**Validation Rules**:
- Only one AboutPage record allowed (enforced in usecase layer)
- Editable only by admin role users

---

## Association Tables

### post_categories (Many-to-Many)

Links posts to categories.

**Attributes**:
- `post_id` (Integer, Foreign Key → Post.id, Primary Key)
- `category_id` (Integer, Foreign Key → Category.id, Primary Key)

**Indexes**:
- Primary key on `(post_id, category_id)`
- `idx_pc_category` on `category_id` (for reverse lookups: posts in category)

---

## Data Integrity Rules

1. **Cascade Deletes**:
   - Delete User → Cascade delete Comments, Reactions (Posts remain with author_id=null or reassign to system user)
   - Delete Post → Cascade delete Comments, Reactions, post_categories associations
   - Delete Category → Remove from post_categories (do not delete posts)

2. **Referential Integrity**:
   - All foreign keys enforce ON DELETE CASCADE or ON DELETE SET NULL
   - SQLAlchemy relationship definitions include `cascade="all, delete-orphan"` where appropriate

3. **Unique Constraints**:
   - User: `(email)`, `(username)`
   - Category: `(name)`, `(slug)`
   - Reaction: `(post_id, user_id, type)` (prevent duplicate reactions)

4. **Check Constraints** (optional, enforced in application layer):
   - `Post.status IN ('draft', 'published')`
   - `Reaction.type IN ('like', 'haha', 'angry', 'sad')`
   - `User.role IN ('author', 'admin')`

---

## Example SQLAlchemy Models (Snippet)

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Table, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class PostStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"

class ReactionType(enum.Enum):
    LIKE = "like"
    HAHA = "haha"
    ANGRY = "angry"
    SAD = "sad"

post_categories = Table(
    "post_categories",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="author")
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    reactions = relationship("Reaction", back_populates="user", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    status: Mapped[PostStatus] = mapped_column(Enum(PostStatus), default=PostStatus.DRAFT, index=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), index=True)
    published_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    
    author = relationship("User", back_populates="posts")
    categories = relationship("Category", secondary=post_categories, back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    reactions = relationship("Reaction", back_populates="post", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_post_status_created", "status", "created_at"),
    )

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    
    posts = relationship("Post", secondary=post_categories, back_populates="categories")

class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")
    
    __table_args__ = (
        Index("idx_comment_post_created", "post_id", "created_at"),
    )

class Reaction(Base):
    __tablename__ = "reactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type: Mapped[ReactionType] = mapped_column(Enum(ReactionType), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    
    post = relationship("Post", back_populates="reactions")
    user = relationship("User", back_populates="reactions")
    
    __table_args__ = (
        Index("idx_reaction_post_type", "post_id", "type"),
        Index("unique_reaction", "post_id", "user_id", "type", unique=True),
    )
```

---

## Migration Strategy

**Initial Migration** (Alembic):
1. Create all tables with indexes and foreign keys
2. Seed 3 users, 5 categories via `scripts/seed_data.py`
3. Generate 10 posts with randomized content, timestamps, and categories

**Future Migrations**:
- Add `AboutPage` table (if needed; alternative: single JSON config)
- Add `Session` table for server-side session storage
- Add full-text search indexes on `Post.title` and `Post.content` (MySQL FULLTEXT or external search engine)

**Rollback Strategy**:
- All Alembic migrations must include `downgrade()` function
- Test migrations on staging environment before production
- Database backups before running migrations in production

---

**Phase 1 Data Model Complete** ✅  
Entities defined with attributes, relationships, validation rules, and indexes. Proceed to API Contracts.
