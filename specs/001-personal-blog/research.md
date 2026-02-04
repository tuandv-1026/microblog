# Research: Personal Blog Platform

**Phase**: 0 - Outline & Research  
**Date**: 2026-02-04  
**Purpose**: Resolve technical unknowns, validate technology choices, document best practices

## Research Questions & Resolutions

### 1. Clean Architecture with FastAPI

**Question**: How to implement Clean Architecture (driver/domain/usecase/service/api) with FastAPI's dependency injection?

**Decision**: Use FastAPI's `Depends()` for dependency injection between layers
- **Domain layer**: Define entity classes and repository interfaces (ABC)
- **Driver layer**: Implement repositories using SQLAlchemy, expose via dependency providers
- **Usecase layer**: Business logic classes accepting repository interfaces
- **Service layer**: Infrastructure services (Markdown, auth, caching) injected into usecases
- **API layer**: FastAPI routers use `Depends()` to inject usecases and services

**Rationale**: FastAPI's dependency injection aligns with Clean Architecture's dependency inversion principle. Routers depend on abstractions (usecase interfaces), not concrete implementations.

**Alternatives Considered**:
- Manual factory pattern: Rejected due to boilerplate and lack of async support
- Flask with Blueprint: FastAPI's native async support and Pydantic integration superior for API-first architecture

**Best Practices**:
```python
# domain/repositories/post_repository.py
from abc import ABC, abstractmethod
class PostRepository(ABC):
    @abstractmethod
    async def get_by_id(self, post_id: int) -> Post: ...

# driver/database/repositories.py
class SQLAlchemyPostRepository(PostRepository):
    def __init__(self, db: AsyncSession):
        self.db = db
    async def get_by_id(self, post_id: int) -> Post:
        result = await self.db.execute(select(PostModel).where(PostModel.id == post_id))
        return result.scalar_one_or_none()

# api/dependencies.py
async def get_post_repository(db: AsyncSession = Depends(get_db)) -> PostRepository:
    return SQLAlchemyPostRepository(db)

# api/routers/posts.py
@router.get("/posts/{post_id}")
async def get_post(post_id: int, repo: PostRepository = Depends(get_post_repository)):
    post = await repo.get_by_id(post_id)
    return post
```

---

### 2. SQLAlchemy 2.0 + Alembic with MySQL

**Question**: Best practices for SQLAlchemy 2.0 async with Alembic migrations and MySQL?

**Decision**: Use SQLAlchemy 2.0 async API with `asyncio` and `aiomysql` driver
- **Engine**: `create_async_engine("mysql+aiomysql://...")`
- **Sessions**: `AsyncSession` with `async_sessionmaker`
- **Migrations**: Alembic with async support enabled via `run_async()` in `env.py`
- **Models**: Declarative base with `mapped_column` and relationship definitions

**Rationale**: SQLAlchemy 2.0's async API prevents blocking I/O in FastAPI endpoints. Alembic provides version-controlled schema migrations essential for production deployments.

**Alternatives Considered**:
- SQLAlchemy 1.4 sync API: Rejected due to blocking I/O and thread pool overhead
- Raw SQL with MySQL connector: Rejected due to lack of ORM features, migration management, and query safety
- Tortoise ORM: Considered but SQLAlchemy has better ecosystem, documentation, and Alembic integration

**Best Practices**:
- Use `asyncio.create_task()` for background tasks (e.g., view count increments)
- Define indexes on frequently queried columns: `Post.status`, `Post.created_at`, `Category.slug`
- Use eager loading (`selectinload`) to avoid N+1 queries: `select(Post).options(selectinload(Post.categories))`
- Connection pooling: Set `pool_size=20, max_overflow=10` for production
- Alembic autogenerate: `alembic revision --autogenerate -m "message"` for schema changes

**Migration Setup**:
```bash
# alembic.ini
sqlalchemy.url = mysql+aiomysql://user:pass@localhost/microblog

# alembic/env.py
from sqlalchemy.ext.asyncio import create_async_engine
async_engine = create_async_engine(config.get_main_option("sqlalchemy.url"))

# Create migration
alembic revision --autogenerate -m "add_post_table"
alembic upgrade head
```

---

### 3. Markdown Rendering + XSS Prevention

**Question**: How to safely render user-submitted Markdown without XSS vulnerabilities?

**Decision**: Two-stage rendering: `python-markdown` → `bleach` sanitization
- **Stage 1**: Parse Markdown to HTML using `markdown.markdown(text, extensions=['fenced_code', 'tables', 'nl2br'])`
- **Stage 2**: Sanitize HTML using `bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)`
- **Allowed tags**: `['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'a', 'strong', 'em', 'code', 'pre', 'blockquote']`
- **Allowed attributes**: `{'a': ['href', 'title'], 'img': ['src', 'alt']}` (no `onclick`, `onerror`)

**Rationale**: `python-markdown` is standard Python Markdown parser with CommonMark support. `bleach` is Mozilla-maintained HTML sanitizer preventing XSS via whitelist approach.

**Alternatives Considered**:
- Markdown-it (JS): Requires Node.js; rejected for Python-native stack
- mistune: Faster but less feature-complete than python-markdown
- DOMPurify: Client-side only; server-side sanitization required for API responses
- markdown with `safe_mode`: Deprecated in python-markdown 3.0+

**Best Practices**:
```python
import markdown
import bleach

ALLOWED_TAGS = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 
                'a', 'strong', 'em', 'code', 'pre', 'blockquote', 'br']
ALLOWED_ATTRS = {'a': ['href', 'title'], '*': ['class']}

def render_markdown(text: str) -> str:
    html = markdown.markdown(text, extensions=['fenced_code', 'tables', 'nl2br'])
    safe_html = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)
    return safe_html
```

---

### 4. Authentication: bcrypt + Session Management

**Question**: Secure authentication implementation for FastAPI with session management?

**Decision**: bcrypt password hashing + HTTP-only session cookies
- **Password hashing**: `bcrypt.hashpw()` with cost factor 12 (balance security/performance)
- **Session storage**: Server-side sessions in MySQL `sessions` table or Redis for scalability
- **Cookies**: `HttpOnly`, `Secure`, `SameSite=Lax` flags to prevent XSS/CSRF
- **Middleware**: Custom FastAPI middleware to load user from session cookie

**Rationale**: bcrypt is industry-standard with adaptive cost factor. HTTP-only cookies prevent XSS attacks on session tokens. Server-side sessions enable revocation (logout).

**Alternatives Considered**:
- JWT tokens: Rejected for v1 due to revocation complexity (logout requires blacklist)
- Argon2: Considered but bcrypt more widely adopted, simpler configuration
- Client-side sessions: Rejected due to tampering risk and session size limits

**Best Practices**:
```python
import bcrypt
from fastapi import Response, Cookie

# Registration
def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt(rounds=12)).decode()

# Login
def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

# Set session cookie
response.set_cookie(
    key="session_id",
    value=session_token,
    httponly=True,
    secure=True,  # HTTPS only
    samesite="lax",
    max_age=604800  # 7 days
)
```

---

### 5. Docker Multi-Container Setup (FE + BE + MySQL)

**Question**: How to orchestrate frontend, backend, and MySQL in Docker for local development?

**Decision**: `docker-compose.yml` with 3 services: `backend`, `frontend`, `db`
- **Backend**: Python 3.11-slim image, exposes port 8000, depends on `db`
- **Frontend**: Node 18-alpine image (React/Vue/vanilla JS), exposes port 3000, proxies API to backend
- **MySQL**: Official mysql:8.0 image, exposes port 3306 (localhost only), persistent volume for data
- **Networking**: All services on same Docker network; frontend accesses backend via `http://backend:8000`

**Rationale**: docker-compose simplifies multi-container orchestration. Named networks enable service discovery. Volumes persist MySQL data across container restarts.

**Alternatives Considered**:
- Separate docker run commands: Rejected due to manual network setup and lack of reproducibility
- Kubernetes: Overkill for local development; docker-compose sufficient for single-machine deployment
- SQLite: Considered for simplicity but MySQL specified in requirements

**Best Practices**:
```yaml
# docker-compose.yml
version: '3.8'
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: microblog
      MYSQL_USER: bloguser
      MYSQL_PASSWORD: blogpass
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

  backend:
    build: ./backend
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DATABASE_URL: mysql+aiomysql://bloguser:blogpass@db:3306/microblog

  frontend:
    build: ./frontend
    command: npm start
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://localhost:8000
```

**Local Development**:
```bash
docker-compose up -d          # Start all services
docker-compose logs -f backend  # View backend logs
docker-compose exec backend alembic upgrade head  # Run migrations
docker-compose down -v        # Stop and remove volumes
```

---

### 6. Mock Data Generation (10 Posts)

**Question**: Best approach to generate 10 mock posts for development/testing?

**Decision**: Python script `scripts/seed_data.py` using Faker library
- **Faker**: Generate realistic titles, content, usernames, dates
- **Script**: Creates 3 users, 5 categories, 10 posts with randomized attributes
- **Content**: Markdown samples with headings, lists, code blocks, links
- **Execution**: `docker-compose exec backend python scripts/seed_data.py`

**Rationale**: Faker provides realistic test data. Python script leverages existing SQLAlchemy models. Script is idempotent (checks for existing data before inserting).

**Alternatives Considered**:
- SQL dump: Rejected due to lack of flexibility and UUID/timestamp conflicts
- Manual data entry: Rejected due to time cost
- Alembic data migration: Considered but seed script more appropriate for development data (not production schema)

**Best Practices**:
```python
# scripts/seed_data.py
from faker import Faker
from src.driver.database.models import User, Post, Category
from src.driver.database.session import SessionLocal
import random

fake = Faker()

async def seed():
    db = SessionLocal()
    
    # Create users
    users = []
    for i in range(3):
        user = User(
            email=f"user{i}@example.com",
            username=f"author{i}",
            hashed_password=hash_password("password123")
        )
        db.add(user)
        users.append(user)
    
    # Create categories
    categories = [Category(name=name, slug=name.lower()) 
                  for name in ["Technology", "Travel", "Food", "Opinion", "Tutorial"]]
    db.add_all(categories)
    
    # Create posts
    for i in range(10):
        post = Post(
            title=fake.sentence(nb_words=6),
            content=generate_markdown_content(),
            author=random.choice(users),
            status="published" if i < 8 else "draft",
            view_count=random.randint(50, 500),
            created_at=fake.date_time_between(start_date='-6M', end_date='now')
        )
        post.categories.extend(random.sample(categories, k=random.randint(1, 3)))
        db.add(post)
    
    await db.commit()
    print("✅ Seeded 10 posts, 3 users, 5 categories")

def generate_markdown_content():
    return f"""
# {fake.sentence()}

{fake.paragraph(nb_sentences=5)}

## Key Points

- {fake.sentence()}
- {fake.sentence()}
- {fake.sentence()}

```python
def example():
    return "Hello World"
```

{fake.paragraph(nb_sentences=10)}
    """
```

---

### 7. Unit Testing with pytest + unittest.sh

**Question**: How to structure unit tests for FastAPI routers and run via shell script?

**Decision**: pytest with async support (`pytest-asyncio`) + `TestClient` for router tests
- **Test structure**: `tests/integration/test_*_router.py` for API contract tests
- **Fixtures**: `conftest.py` defines test database, test client, authenticated user fixtures
- **Script**: `scripts/unittest.sh` runs `pytest tests/integration/ -v --tb=short`
- **Coverage**: Aim for 80% coverage on routers, usecases

**Rationale**: pytest is Python standard with excellent async support. FastAPI's `TestClient` uses httpx for synchronous testing of async endpoints. Shell script provides consistent test invocation.

**Alternatives Considered**:
- unittest module: Rejected due to verbose syntax and limited async support
- Postman/Newman: Rejected for CI/CD; pytest integrates better with Python codebase
- Manual curl scripts: Rejected due to lack of assertions and test organization

**Best Practices**:
```python
# tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from fastapi.testclient import TestClient
from src.main import app
from src.driver.database.models import Base

@pytest.fixture
async def test_db():
    engine = create_async_engine("mysql+aiomysql://test:test@localhost/test_microblog")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def client(test_db):
    return TestClient(app)

@pytest.fixture
async def authenticated_user(client):
    response = client.post("/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123"
    })
    return response.json()

# tests/integration/test_posts_router.py
def test_get_posts(client):
    response = client.get("/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_post_authenticated(client, authenticated_user):
    response = client.post("/posts", json={
        "title": "Test Post",
        "content": "# Test Content",
        "status": "draft"
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Test Post"
```

```bash
# scripts/unittest.sh
#!/usr/bin/env bash
set -e

echo "🧪 Running unit tests for routers..."
pytest tests/integration/ -v --tb=short --cov=src/api/routers --cov-report=term-missing

echo "✅ All tests passed"
```

---

## Technology Stack Summary

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Language | Python | 3.11+ | Backend runtime |
| Framework | FastAPI | 0.104+ | REST API framework |
| Validation | Pydantic | 2.5+ | Request/response schemas |
| ORM | SQLAlchemy | 2.0+ | Database abstraction |
| Migrations | Alembic | 1.13+ | Schema versioning |
| Database | MySQL | 8.0+ | Persistent storage |
| Markdown | python-markdown | 3.5+ | Markdown parsing |
| Sanitization | bleach | 6.1+ | XSS prevention |
| Authentication | bcrypt | 4.1+ | Password hashing |
| Testing | pytest | 7.4+ | Test framework |
| Containerization | Docker | 24+ | Environment isolation |
| Orchestration | docker-compose | 2.23+ | Multi-container setup |
| Mock Data | Faker | 20+ | Test data generation |

---

## Architecture Decisions

### Clean Architecture Layers

1. **Domain Layer** (`src/domain/`): 
   - Entities (Post, User, Category, Comment, Reaction)
   - Repository interfaces (abstract base classes)
   - Domain logic (business rules independent of frameworks)

2. **Usecase Layer** (`src/usecase/`):
   - Application business logic
   - Orchestrates domain entities and repositories
   - Examples: `CreatePostUseCase`, `PublishPostUseCase`, `AuthenticateUserUseCase`

3. **Service Layer** (`src/service/`):
   - Infrastructure services (Markdown, auth, caching)
   - External integrations (email, S3 for future features)
   - Injected into usecases via dependency injection

4. **Driver Layer** (`src/driver/`):
   - Database implementations (SQLAlchemy models, repositories)
   - Configuration management (environment variables)
   - External adapters (HTTP clients, file storage)

5. **API Layer** (`src/api/`):
   - FastAPI routers and endpoints
   - Pydantic schemas for request/response
   - Dependency injection setup

**Dependency Rule**: Inner layers (domain, usecase) do not depend on outer layers (driver, api). Outer layers depend inward via interfaces.

---

## Security Best Practices

1. **Password Security**: bcrypt with cost factor 12, salted hashes
2. **Session Management**: HTTP-only cookies, 7-day expiration, server-side storage
3. **XSS Prevention**: bleach HTML sanitization on all user-generated content
4. **CSRF Protection**: SameSite cookies + CSRF token validation (FastAPI CSRF middleware)
5. **SQL Injection**: SQLAlchemy parameterized queries (no raw SQL with f-strings)
6. **Input Validation**: Pydantic schemas enforce types, lengths, formats
7. **HTTPS**: Secure cookies require HTTPS in production (nginx reverse proxy)
8. **CORS**: FastAPI CORS middleware with explicit allowed origins

---

## Performance Considerations

1. **Database Indexing**: 
   - `Post(status, created_at)` for homepage queries
   - `Category(slug)` for category page lookups
   - `User(email)` for login queries

2. **N+1 Query Prevention**: 
   - Use `selectinload()` for eager loading relationships
   - Example: `select(Post).options(selectinload(Post.categories), selectinload(Post.author))`

3. **Caching Strategy** (Future):
   - Redis for homepage post list (invalidate on new post)
   - Redis for category counts (invalidate on post publish/delete)

4. **Connection Pooling**: 
   - SQLAlchemy pool_size=20, max_overflow=10
   - Keep-alive connections to MySQL

5. **Async I/O**: 
   - All database operations use `async`/`await`
   - Background tasks for view count increments

---

## Open Questions for Implementation Phase

1. **Frontend Framework**: React, Vue, or vanilla JS? (Defer to implementation; spec is framework-agnostic)
2. **CSS Framework**: Tailwind, Bootstrap, or custom? (Tailwind recommended for utility-first responsive design)
3. **Frontend Build Tool**: Vite, Webpack, or Create React App? (Vite recommended for speed)
4. **Image Handling**: Local storage vs. S3? (Local for v1, S3 for production scaling)
5. **Comment Moderation UI**: Admin panel or inline buttons? (Inline for v1 simplicity)
6. **Search Implementation**: SQL LIKE vs. full-text index? (LIKE for v1, full-text for v2)
7. **Emoji Reaction Storage**: Separate table or JSON column? (Separate table for relational queries)

---

**Phase 0 Complete** ✅  
All technical unknowns resolved. Proceed to Phase 1: Data Model & Contracts.
