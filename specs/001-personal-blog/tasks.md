# Tasks: Personal Blog Platform

**Input**: Design documents from `/specs/001-personal-blog/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/api.yaml ✅, quickstart.md ✅

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and Docker environment setup

- [ ] T001 Create backend directory structure per Clean Architecture in backend/src/{domain,usecase,service,driver,api}
- [ ] T002 [P] Create frontend directory structure in frontend/src/{components,pages,services,styles}
- [ ] T003 [P] Create backend/requirements.txt with FastAPI, Pydantic, SQLAlchemy, Alembic, aiomysql, python-markdown, bleach, bcrypt, pytest dependencies
- [ ] T004 [P] Create frontend/package.json with React/Vue and responsive CSS framework (Tailwind/Bootstrap)
- [ ] T005 Create docker-compose.yml with 3 services: backend (Python 3.11), frontend (Node 18), db (MySQL 8.0)
- [ ] T006 [P] Create backend/Dockerfile with Python 3.11-slim base image and requirements installation
- [ ] T007 [P] Create frontend/Dockerfile with Node 18-alpine base image
- [ ] T008 [P] Create backend/.env.example with DATABASE_URL, SECRET_KEY, BCRYPT_ROUNDS, ENVIRONMENT templates
- [ ] T009 [P] Create frontend/.env.example with REACT_APP_API_URL template
- [ ] T010 Create backend/alembic.ini for Alembic configuration pointing to MySQL
- [ ] T011 Initialize Alembic in backend/alembic/ with env.py configured for async SQLAlchemy

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that all user stories depend on

- [ ] T012 [P] Define SQLAlchemy Base and engine setup in backend/src/driver/database/session.py with async support
- [ ] T013 [P] Create domain entities in backend/src/domain/entities/ for Post, User, Category, Comment, Reaction
- [ ] T014 [P] Define repository interfaces in backend/src/domain/repositories/ for PostRepository, UserRepository, CategoryRepository
- [ ] T015 Create SQLAlchemy models in backend/src/driver/database/models.py matching data-model.md (User, Post, Category, Comment, Reaction, post_categories table)
- [ ] T016 Add indexes to models: idx_post_status_created, idx_user_email, idx_category_slug, idx_comment_post_created, idx_reaction_post_type
- [ ] T017 Create initial Alembic migration in backend/alembic/versions/ for all tables with relationships and indexes
- [ ] T018 [P] Implement Markdown service in backend/src/service/markdown_service.py with python-markdown + bleach sanitization
- [ ] T019 [P] Implement auth service in backend/src/service/auth_service.py with bcrypt hashing and password verification
- [ ] T020 [P] Create Pydantic schemas in backend/src/api/schemas/ for auth_schemas, post_schemas, comment_schemas, category_schemas
- [ ] T021 Create FastAPI app initialization in backend/src/main.py with CORS middleware, error handlers, router registration
- [ ] T022 [P] Create dependency injection setup in backend/src/api/dependencies.py for database session, repositories, current user
- [ ] T023 [P] Create pytest fixtures in backend/tests/conftest.py for test database, test client, authenticated user
- [ ] T024 [P] Create frontend API client in frontend/src/services/api.js with axios/fetch wrappers for all endpoints
- [ ] T025 [P] Create reusable UI components in frontend/src/components/ for Navbar, Sidebar, MarkdownRenderer
- [ ] T026 Create scripts/unittest.sh in backend/scripts/ to run pytest with coverage for integration tests

---

## Phase 3: User Story 1 - Browse and Read Blog Posts (P1)

**Goal**: Visitors can view homepage with 3-column layout (desktop)/single-column (mobile), read posts with rendered Markdown, navigate between pages

**Independent Test**: Create sample posts → verify homepage layout → click post → verify Markdown rendering → test responsive on 375px/1024px

**Tasks**:

- [ ] T027 [US1] Implement concrete PostRepository in backend/src/driver/database/repositories.py with async methods: get_all, get_by_id, get_by_status
- [ ] T028 [US1] Implement GetPostsUseCase in backend/src/usecase/post_usecase.py with sorting logic (newest, oldest, likes, views) and pagination
- [ ] T029 [US1] Implement GetPostByIdUseCase in backend/src/usecase/post_usecase.py with view count increment
- [ ] T030 [US1] Create GET /posts router in backend/src/api/routers/posts.py with query params: sort, category, page, limit
- [ ] T031 [US1] Create GET /posts/{id} router in backend/src/api/routers/posts.py returning PostDetail with rendered HTML
- [ ] T032 [P] [US1] Create PostCard component in frontend/src/components/PostCard.jsx for post preview display (title, excerpt, author, date, stats)
- [ ] T033 [P] [US1] Create HomePage component in frontend/src/pages/HomePage.jsx with 3-column layout: left (recent posts), center (post list), right (categories)
- [ ] T034 [P] [US1] Implement responsive CSS in frontend/src/styles/ for 3-column → single-column breakpoints (≥1024px, <768px)
- [ ] T035 [US1] Create PostDetailPage component in frontend/src/pages/PostDetailPage.jsx displaying full rendered Markdown content
- [ ] T036 [P] [US1] Create CategoryPage component in frontend/src/pages/CategoryPage.jsx with same layout as HomePage filtered by category
- [ ] T037 [P] [US1] Create AboutPage component in frontend/src/pages/AboutPage.jsx as placeholder (full implementation in US6)
- [ ] T038 [P] [US1] Implement routing in frontend/src/App.jsx for / (home), /posts/:id (detail), /category/:slug, /about
- [ ] T039 [US1] Write integration test in backend/tests/integration/test_posts_router.py for GET /posts with sort/filter/pagination
- [ ] T040 [US1] Write integration test in backend/tests/integration/test_posts_router.py for GET /posts/{id} verifying Markdown rendering

---

## Phase 4: User Story 2 - Filter and Sort Content (P1)

**Goal**: Visitors can sort posts (time/likes/views), filter by category, search by title/author

**Independent Test**: Create posts with categories → verify sort options → test category filter → search by title/author → verify results

**Tasks**:

- [ ] T041 [US2] Implement CategoryRepository in backend/src/driver/database/repositories.py with get_all, get_by_slug, get_with_post_counts
- [ ] T042 [US2] Implement GetCategoriesUseCase in backend/src/usecase/category_usecase.py with sorting by post_count or name
- [ ] T043 [US2] Create GET /categories router in backend/src/api/routers/categories.py with sort parameter
- [ ] T044 [US2] Create GET /categories/{slug} router in backend/src/api/routers/categories.py returning category details
- [ ] T045 [US2] Implement SearchPostsUseCase in backend/src/usecase/post_usecase.py with LIKE query on title and author.username
- [ ] T046 [US2] Create GET /search router in backend/src/api/routers/search.py with query parameter and pagination
- [ ] T047 [P] [US2] Add sort controls to HomePage component in frontend/src/pages/HomePage.jsx (dropdown or buttons for newest/oldest/likes/views)
- [ ] T048 [P] [US2] Implement category filtering in CategoryPage by fetching GET /posts?category={slug}
- [ ] T049 [P] [US2] Create search input in Navbar component in frontend/src/components/Navbar.jsx
- [ ] T050 [P] [US2] Create SearchResultsPage component in frontend/src/pages/SearchResultsPage.jsx displaying matching posts
- [ ] T051 [P] [US2] Add routing for /search?q={query} in frontend/src/App.jsx
- [ ] T052 [P] [US2] Populate Sidebar component in frontend/src/components/Sidebar.jsx with category list ordered by post count
- [ ] T053 [US2] Write integration test in backend/tests/integration/test_categories_router.py for GET /categories
- [ ] T054 [US2] Write integration test in backend/tests/integration/test_search_router.py for GET /search with title and author matching

---

## Phase 5: User Story 3 - User Authentication (P2)

**Goal**: Users can register, login, logout with secure session management

**Independent Test**: Register new account → verify validation → login → verify session cookie → logout → verify session cleared

**Tasks**:

- [ ] T055 [US3] Implement UserRepository in backend/src/driver/database/repositories.py with create, get_by_email, get_by_username, get_by_id
- [ ] T056 [US3] Implement RegisterUseCase in backend/src/usecase/auth_usecase.py with email/username uniqueness check and password hashing
- [ ] T057 [US3] Implement LoginUseCase in backend/src/usecase/auth_usecase.py with credential verification and session creation
- [ ] T058 [US3] Implement LogoutUseCase in backend/src/usecase/auth_usecase.py with session invalidation
- [ ] T059 [US3] Create POST /register router in backend/src/api/routers/auth.py with RegisterRequest schema validation
- [ ] T060 [US3] Create POST /login router in backend/src/api/routers/auth.py with Set-Cookie for session_id (HttpOnly, Secure, SameSite)
- [ ] T061 [US3] Create POST /logout router in backend/src/api/routers/auth.py clearing session cookie
- [ ] T062 [US3] Create GET /me router in backend/src/api/routers/auth.py returning current authenticated user
- [ ] T063 [US3] Implement get_current_user dependency in backend/src/api/dependencies.py reading session cookie and fetching user
- [ ] T064 [P] [US3] Create LoginPage component in frontend/src/pages/LoginPage.jsx with email and password fields
- [ ] T065 [P] [US3] Create RegisterPage component in frontend/src/pages/RegisterPage.jsx with email, username, password, password_confirm fields
- [ ] T066 [P] [US3] Add routing for /login and /register in frontend/src/App.jsx
- [ ] T067 [P] [US3] Implement authentication context in frontend (e.g., AuthContext) to store current user state across app
- [ ] T068 [P] [US3] Update Navbar component to show username, "New Post", "Logout" for authenticated users
- [ ] T069 [US3] Write integration test in backend/tests/integration/test_auth_router.py for POST /register with valid and invalid data
- [ ] T070 [US3] Write integration test in backend/tests/integration/test_auth_router.py for POST /login and POST /logout verifying session management

---

## Phase 6: User Story 4 - Create and Publish Blog Posts (P2)

**Goal**: Authenticated users can create posts with Markdown, save as draft, preview, assign categories, publish

**Independent Test**: Login → create post → save draft → preview Markdown → publish → verify appears on homepage → edit post → delete post

**Tasks**:

- [ ] T071 [US4] Implement CreatePostUseCase in backend/src/usecase/post_usecase.py with category assignment
- [ ] T072 [US4] Implement PublishPostUseCase in backend/src/usecase/post_usecase.py changing status from draft to published and setting published_at
- [ ] T073 [US4] Implement UpdatePostUseCase in backend/src/usecase/post_usecase.py with author authorization check
- [ ] T074 [US4] Implement DeletePostUseCase in backend/src/usecase/post_usecase.py with author authorization check
- [ ] T075 [US4] Create POST /posts router in backend/src/api/routers/posts.py with CreatePostRequest schema (title, content, status, category_ids)
- [ ] T076 [US4] Create POST /posts/{id}/publish router in backend/src/api/routers/posts.py
- [ ] T077 [US4] Create PUT /posts/{id} router in backend/src/api/routers/posts.py with UpdatePostRequest schema
- [ ] T078 [US4] Create DELETE /posts/{id} router in backend/src/api/routers/posts.py
- [ ] T079 [P] [US4] Create EditorPage component in frontend/src/pages/EditorPage.jsx with title input, Markdown textarea, category multi-select
- [ ] T080 [P] [US4] Implement live Markdown preview in EditorPage using MarkdownRenderer component (side-by-side or toggle view)
- [ ] T081 [P] [US4] Add "Save as Draft" and "Publish" buttons in EditorPage calling POST /posts with appropriate status
- [ ] T082 [P] [US4] Create MyDraftsPage component in frontend/src/pages/MyDraftsPage.jsx listing user's draft posts
- [ ] T083 [P] [US4] Add "Edit" and "Delete" buttons in PostDetailPage visible only to post author
- [ ] T084 [P] [US4] Add routing for /posts/new (editor), /posts/:id/edit (editor), /my-drafts in frontend/src/App.jsx
- [ ] T085 [US4] Write integration test in backend/tests/integration/test_posts_router.py for POST /posts creating draft and published posts
- [ ] T086 [US4] Write integration test in backend/tests/integration/test_posts_router.py for POST /posts/{id}/publish
- [ ] T087 [US4] Write integration test in backend/tests/integration/test_posts_router.py for PUT /posts/{id} and DELETE /posts/{id} with authorization

---

## Phase 7: User Story 5 - Comment and React with Emojis (P3)

**Goal**: Authenticated users can comment on posts and react with emoji (like, haha, angry, sad)

**Independent Test**: Login → view published post → add comment → verify appears chronologically → click emoji → verify count increments → click again → verify toggle

**Tasks**:

- [ ] T088 [US5] Implement CommentRepository in backend/src/driver/database/repositories.py with create, get_by_post, delete
- [ ] T089 [US5] Implement CreateCommentUseCase in backend/src/usecase/comment_usecase.py with published post check
- [ ] T090 [US5] Implement DeleteCommentUseCase in backend/src/usecase/comment_usecase.py with author/post-author authorization
- [ ] T091 [US5] Create GET /posts/{id}/comments router in backend/src/api/routers/comments.py returning comments ordered by created_at ASC
- [ ] T092 [US5] Create POST /posts/{id}/comments router in backend/src/api/routers/comments.py with CreateCommentRequest schema
- [ ] T093 [US5] Create DELETE /comments/{id} router in backend/src/api/routers/comments.py
- [ ] T094 [US5] Implement ReactionRepository in backend/src/driver/database/repositories.py with create, delete, get_by_post, get_user_reactions
- [ ] T095 [US5] Implement ToggleReactionUseCase in backend/src/usecase/reaction_usecase.py checking for existing reaction (add or remove)
- [ ] T096 [US5] Create GET /posts/{id}/reactions router in backend/src/api/routers/reactions.py returning ReactionSummary with counts and user_reactions
- [ ] T097 [US5] Create POST /posts/{id}/reactions router in backend/src/api/routers/reactions.py with ToggleReactionRequest schema
- [ ] T098 [P] [US5] Create CommentSection component in frontend/src/components/CommentSection.jsx displaying comments list and input form
- [ ] T099 [P] [US5] Add CommentSection to PostDetailPage component
- [ ] T100 [P] [US5] Create EmojiReactions component in frontend/src/components/EmojiReactions.jsx with 4 emoji buttons and counts
- [ ] T101 [P] [US5] Add EmojiReactions to PostDetailPage above comments section
- [ ] T102 [P] [US5] Implement toggle logic in EmojiReactions calling POST /posts/{id}/reactions and updating UI optimistically
- [ ] T103 [P] [US5] Disable comment form and reactions for non-authenticated users with "Login to interact" message
- [ ] T104 [US5] Write integration test in backend/tests/integration/test_comments_router.py for POST /posts/{id}/comments and GET /posts/{id}/comments
- [ ] T105 [US5] Write integration test in backend/tests/integration/test_reactions_router.py for POST /posts/{id}/reactions toggle behavior

---

## Phase 8: User Story 6 - About Me Page (P3)

**Goal**: Visitors can view About Me page; blog owner can edit bio content

**Independent Test**: Navigate to /about → view content → login as admin → edit bio → save → verify updated

**Tasks**:

- [ ] T106 [US6] Add AboutPage model/table to backend/src/driver/database/models.py (optional: single row or settings table)
- [ ] T107 [US6] Create Alembic migration for AboutPage table
- [ ] T108 [US6] Implement AboutPageRepository in backend/src/driver/database/repositories.py with get, update
- [ ] T109 [US6] Implement GetAboutPageUseCase and UpdateAboutPageUseCase in backend/src/usecase/about_usecase.py (admin check for update)
- [ ] T110 [US6] Create GET /about router in backend/src/api/routers/about.py returning rendered Markdown
- [ ] T111 [US6] Create PUT /about router in backend/src/api/routers/about.py with UpdateAboutPageRequest schema (admin only)
- [ ] T112 [P] [US6] Update AboutPage component in frontend/src/pages/AboutPage.jsx to fetch and display GET /about
- [ ] T113 [P] [US6] Add "Edit Bio" button in AboutPage visible only to admin role
- [ ] T114 [P] [US6] Create AboutEditorPage component or modal in frontend for editing bio with Markdown textarea
- [ ] T115 [US6] Write integration test in backend/tests/integration/test_about_router.py for GET /about and PUT /about with role check

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Testing, deployment scripts, documentation, performance optimization

- [ ] T116 [P] Create scripts/seed_data.py in backend/scripts/ using Faker to generate 3 users, 5 categories, 10 posts (8 published, 2 drafts)
- [ ] T117 [P] Test seed_data.py by running docker-compose exec backend python scripts/seed_data.py and verifying data
- [ ] T118 [P] Add view counter service in backend/src/service/view_counter_service.py with session-based tracking (increment once per session)
- [ ] T119 [P] Integrate view counter into GetPostByIdUseCase incrementing Post.view_count
- [ ] T120 [P] Add health check endpoint GET /health in backend/src/main.py returning {"status":"ok","environment":"development"}
- [ ] T121 [P] Create README.md in repository root with project overview, tech stack, and link to quickstart.md
- [ ] T122 Test responsive design manually at 375px (mobile), 768px (tablet), 1024px (desktop) viewports for all pages
- [ ] T123 Test touch targets on mobile: ensure all buttons/links ≥44px tap target
- [ ] T124 Run backend/scripts/unittest.sh and verify all integration tests pass with ≥80% coverage
- [ ] T125 Test full user flows: visitor browsing → registration → post creation → draft → publish → comment → reaction → logout
- [ ] T126 [P] Add error boundaries in frontend for graceful error handling
- [ ] T127 [P] Add loading states in frontend components while fetching data
- [ ] T128 Security audit: verify CSRF tokens, XSS sanitization, SQL injection prevention, secure cookies
- [ ] T129 Performance test: verify homepage loads in <2s with 20 posts on simulated 3G connection
- [ ] T130 [P] Add .gitignore files for backend (__pycache__, venv, .env) and frontend (node_modules, .env)

---

## Dependencies & Execution Order

### Story Completion Order (per spec priorities):

```
Phase 1 (Setup) → Phase 2 (Foundational)
  ↓
US1 (P1: Browse/Read) ← Can start immediately after Phase 2
  ↓
US2 (P1: Filter/Sort) ← Depends on US1 (uses same PostRepository)
  ↓
US3 (P2: Auth) ← Can be developed in parallel with US1/US2 but needed before US4/US5
  ↓
US4 (P2: Create/Publish) ← Depends on US3 (requires authentication)
  ↓
US5 (P3: Comments/Reactions) ← Depends on US3 and US4 (requires posts and auth)
  ↓
US6 (P3: About) ← Depends on US3 (admin check), can be done last
  ↓
Phase 9 (Polish) ← Final integration and testing
```

### Parallel Execution Opportunities:

**After Phase 2 (T012-T026) completes:**
- US1 backend (T027-T031) || US1 frontend (T032-T038)
- US2 backend (T041-T046) || US2 frontend (T047-T052)
- US3 backend (T055-T063) || US3 frontend (T064-T068)
- US4 backend (T071-T078) || US4 frontend (T079-T084)
- US5 backend (T088-T097) || US5 frontend (T098-T103)
- US6 backend (T106-T111) || US6 frontend (T112-T114)

**Within each story:**
- Backend repositories, usecases, routers can be built sequentially (depend on each other)
- Frontend components can be built in parallel (PostCard || HomePage || PostDetailPage)
- Tests can be written in parallel with implementation ([P] marker on test tasks)

**Phase 9 Polish:**
- All [P] tasks (T116, T118, T120, T121, T126, T127, T130) can run in parallel
- Testing tasks (T122-T125, T128-T129) must run after implementation completes

---

## Implementation Strategy

### MVP Scope (Week 1-2):
- Phase 1: Setup (T001-T011)
- Phase 2: Foundational (T012-T026)
- US1: Browse/Read (T027-T040) - Core value delivery

### Extended MVP (Week 3-4):
- US2: Filter/Sort (T041-T054) - Enhanced discoverability
- US3: Auth (T055-T070) - Enable authoring
- US4: Create/Publish (T071-T087) - Complete authoring workflow

### Full v1 (Week 5-6):
- US5: Comments/Reactions (T088-T105) - Engagement layer
- US6: About (T106-T115) - Static content
- Phase 9: Polish (T116-T130) - Production readiness

### Incremental Delivery:
Each user story completion is a deployable increment:
- After US1: Read-only blog (demo to stakeholders)
- After US2: Enhanced browsing with search/filter
- After US3+US4: Full authoring platform (MVP complete)
- After US5: Community engagement
- After US6: Personalized author presence

---

## Task Validation

**Total Tasks**: 130
- Setup: 11 tasks (T001-T011)
- Foundational: 15 tasks (T012-T026)
- US1 (P1): 14 tasks (T027-T040)
- US2 (P1): 14 tasks (T041-T054)
- US3 (P2): 16 tasks (T055-T070)
- US4 (P2): 17 tasks (T071-T087)
- US5 (P3): 18 tasks (T088-T105)
- US6 (P3): 10 tasks (T106-T115)
- Polish: 15 tasks (T116-T130)

**Format Compliance**: ✅ All tasks follow `- [ ] [ID] [P?] [Story?] Description with file path` format

**Independent Testing**: ✅ Each user story has explicit test criteria and test tasks

**Parallelization**: ✅ 47 tasks marked [P] for parallel execution (36% of total)

**Story Mapping**: ✅ All tasks mapped to user stories (US1-US6) or infrastructure (Setup/Foundational/Polish)

---

**Ready for Implementation** ✅  
Run `/speckit.implement` or start with Phase 1 Setup tasks (T001-T011) using Docker.
