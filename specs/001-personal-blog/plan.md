# Implementation Plan: Personal Blog Platform

**Branch**: `001-personal-blog` | **Date**: 2026-02-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-personal-blog/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a responsive personal blog platform with Markdown rendering, user authentication, draft/publish workflow, category filtering, search, commenting, and emoji reactions. The system uses Clean Architecture with FastAPI backend (Python 3.11+), MySQL database, and containerized deployment via Docker. Frontend is a responsive web application with 3-column desktop layout adapting to single-column mobile view. Core features prioritized: read-only browsing (P1), content filtering/search (P1), authentication (P2), authoring (P2), engagement features (P3).

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI 0.104+, Pydantic 2.5+, SQLAlchemy 2.0+, Alembic 1.13+, python-markdown 3.5+, bleach 6.1+ (HTML sanitization), pytest 7.4+  
**Storage**: MySQL 8.0+ (relational database for posts, users, comments, reactions, categories)  
**Testing**: pytest with pytest-asyncio for async tests, unittest.sh script for running router/API tests  
**Target Platform**: Linux/macOS server, containerized via Docker (docker-compose for local FE+BE orchestration)  
**Project Type**: Web application (backend API + frontend)  
**Performance Goals**: Homepage load <2s on 3G (20 posts), search results <500ms (1000+ posts), markdown rendering <100ms per post  
**Constraints**: Mobile-first responsive (≥375px), touch targets ≥44px, WCAG AA contrast, secure authentication (bcrypt cost 10+), XSS/CSRF/SQLi prevention  
**Scale/Scope**: Single-user blog (extensible to multi-user), ~10-100 posts initially, 10 mock posts for development, MVP focuses on P1/P2 user stories

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Content-First Architecture ✅
- **Alignment**: Post entity is central to data model with explicit draft/published state transitions
- **Implementation**: SQLAlchemy models define Post with status field, timestamps (created_at, published_at), relationships to Category (many-to-many) and Comment/Reaction (one-to-many)
- **Markdown Storage**: Raw Markdown stored in Post.content field; rendering happens in API layer via python-markdown library

### User-Centric UX (NON-NEGOTIABLE) ✅
- **Alignment**: Frontend uses responsive CSS (Tailwind or Bootstrap) with mobile-first breakpoints
- **Implementation**: 3-column layout (≥1024px) collapses to single-column (<768px), touch targets ≥44px, forms optimized for mobile keyboards
- **Testing**: Manual responsive testing required at 375px, 768px, 1024px viewports before deployment

### Moderation-Ready ⚠️ PARTIAL
- **Current Scope**: Comments appear immediately without moderation (FR-032 to FR-036)
- **Constitution Requirement**: Comments should default to pending approval
- **Resolution**: v1 ships without moderation to prioritize P1/P2 features; moderation capabilities added in future iteration (noted in spec Out of Scope)
- **Risk Mitigation**: Comment form requires authentication (FR-032), reducing spam; delete functionality available to post author

### Markdown-Native ✅
- **Alignment**: Markdown stored as plaintext in database, rendered server-side before API response
- **Implementation**: python-markdown with safe_mode + bleach sanitization prevents XSS
- **Preview**: Editor provides client-side Markdown preview (same rendering logic)

### Simplicity Over Features ✅
- **Alignment**: Implementation focuses on core loop: write → tag → publish → read → comment
- **Deferred Features**: RSS feeds, analytics, multi-user, advanced search, scheduling (all in Out of Scope)
- **Justification**: v1 delivers 6 user stories (45 FRs) targeting MVP; additional features require proven stability first

**Gate Status**: ✅ **PASS WITH NOTES** - Moderation-Ready partially deferred to v2; all other principles aligned. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── domain/              # Domain layer (entities, value objects, domain logic)
│   │   ├── entities/        # Post, User, Category, Comment, Reaction
│   │   └── repositories/    # Abstract repository interfaces
│   ├── usecase/             # Use case layer (application business logic)
│   │   ├── post_usecase.py  # Create/publish/edit/delete posts
│   │   ├── auth_usecase.py  # Register/login/logout
│   │   ├── comment_usecase.py
│   │   └── reaction_usecase.py
│   ├── service/             # Service layer (infrastructure services)
│   │   ├── markdown_service.py  # Markdown rendering + sanitization
│   │   ├── auth_service.py      # Password hashing, session management
│   │   └── view_counter_service.py
│   ├── driver/              # Driver layer (database, external adapters)
│   │   ├── database/
│   │   │   ├── models.py         # SQLAlchemy ORM models
│   │   │   ├── repositories.py   # Concrete repository implementations
│   │   │   └── session.py        # DB session management
│   │   └── config.py             # Environment configuration
│   ├── api/                 # API layer (FastAPI routes, request/response models)
│   │   ├── routers/
│   │   │   ├── posts.py          # POST /posts, GET /posts, GET /posts/{id}
│   │   │   ├── auth.py           # POST /register, POST /login, POST /logout
│   │   │   ├── comments.py       # POST /posts/{id}/comments
│   │   │   ├── reactions.py      # POST /posts/{id}/reactions
│   │   │   ├── categories.py     # GET /categories
│   │   │   └── search.py         # GET /search
│   │   ├── schemas/              # Pydantic request/response models
│   │   │   ├── post_schemas.py
│   │   │   ├── auth_schemas.py
│   │   │   └── comment_schemas.py
│   │   └── dependencies.py       # FastAPI dependency injection
│   └── main.py              # FastAPI app initialization, CORS, middleware
├── alembic/                 # Database migrations
│   ├── versions/            # Migration scripts
│   └── env.py
├── tests/
│   ├── unit/                # Unit tests for usecases, services
│   │   ├── test_post_usecase.py
│   │   ├── test_auth_usecase.py
│   │   └── test_markdown_service.py
│   ├── integration/         # Integration tests for routers (API contract tests)
│   │   ├── test_posts_router.py
│   │   ├── test_auth_router.py
│   │   └── test_comments_router.py
│   └── conftest.py          # Pytest fixtures (test DB, test client)
├── scripts/
│   ├── seed_data.py         # Generate 10 mock posts
│   └── unittest.sh          # Run pytest for router tests
├── Dockerfile
├── docker-compose.yml       # Orchestrate backend + MySQL + frontend
├── requirements.txt
├── alembic.ini
└── .env.example

frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── PostCard.jsx     # Post preview card
│   │   ├── Navbar.jsx       # Navigation menu
│   │   ├── Sidebar.jsx      # Category/recent posts sidebar
│   │   └── MarkdownRenderer.jsx
│   ├── pages/               # Page components
│   │   ├── HomePage.jsx     # 3-column layout with posts
│   │   ├── PostDetailPage.jsx
│   │   ├── CategoryPage.jsx
│   │   ├── AboutPage.jsx
│   │   ├── LoginPage.jsx
│   │   ├── RegisterPage.jsx
│   │   └── EditorPage.jsx   # Post creation/editing
│   ├── services/            # API client
│   │   └── api.js           # Axios/fetch wrappers for backend
│   ├── styles/              # CSS/Tailwind styles
│   └── App.jsx              # Root component, routing
├── public/
├── Dockerfile
├── package.json
└── .env.example
```

**Structure Decision**: Web application structure with Clean Architecture in backend. Backend follows dependency rule: API → Usecase → Domain ← Driver. FastAPI routers depend on usecases via dependency injection; usecases depend on repository interfaces defined in domain; driver layer implements repositories using SQLAlchemy. Frontend is a separate containerized SPA communicating via REST API.

## Complexity Tracking

> **Constitution Check Result**: ✅ PASS WITH NOTES (Moderation-Ready partially deferred)

**No violations requiring justification.** All architectural decisions align with constitution principles:

1. **Content-First Architecture**: Post entity is central with explicit state transitions
2. **User-Centric UX**: Mobile-first responsive design enforced
3. **Moderation-Ready**: Deferred to v2 (acceptable per constitution "Simplicity Over Features")
4. **Markdown-Native**: Raw Markdown storage with rendering at display time
5. **Simplicity Over Features**: MVP focus on core loop, advanced features deferred

**Clean Architecture Layers** (driver/domain/usecase/service/api) chosen to:
- Enforce dependency inversion (outer layers depend on inner abstractions)
- Enable independent testing of business logic (usecases, services)
- Support future scaling (swap repository implementations without changing usecases)
- Align with FastAPI's dependency injection patterns

**Trade-offs Accepted**:
- Clean Architecture adds initial complexity vs. direct MVC, but improves maintainability for multi-user extensibility
- Docker multi-container setup requires orchestration but ensures environment consistency across development/production
- SQLAlchemy 2.0 async has learning curve but prevents blocking I/O in API endpoints

**Rejected Simpler Alternatives**:
- Single-file FastAPI app: Would not scale to 6 user stories with 45 functional requirements
- SQLite + sync SQLAlchemy: Would not support production traffic or concurrent writes
- Manual password hashing: bcrypt library is industry standard, complexity justified by security requirements
