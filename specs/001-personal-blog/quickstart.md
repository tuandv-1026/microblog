# Quickstart: Personal Blog Platform

**Purpose**: Get the development environment running in under 10 minutes  
**Date**: 2026-02-04

## Prerequisites

- **Docker Desktop** 4.25+ (includes docker-compose)
- **Git** (for cloning repository)
- **Port availability**: 3000 (frontend), 8000 (backend), 3306 (MySQL)

Optional for development:
- **Python** 3.11+ (for running backend without Docker)
- **Node.js** 18+ (for running frontend without Docker)

---

## Quick Start (Docker)

### 1. Clone Repository

```bash
git clone <repository-url>
cd microblog
git checkout 001-personal-blog
```

### 2. Set Up Environment Variables

```bash
# Copy example env files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

**backend/.env** (default values work for Docker):
```env
# Database
DATABASE_URL=mysql+aiomysql://bloguser:blogpass@db:3306/microblog

# Security
SECRET_KEY=your-secret-key-change-in-production
BCRYPT_ROUNDS=12

# Environment
ENVIRONMENT=development
DEBUG=true
```

**frontend/.env** (default values work for Docker):
```env
REACT_APP_API_URL=http://localhost:8000
```

### 3. Start All Services

```bash
docker-compose up -d
```

This command:
- Pulls MySQL 8.0 image
- Builds backend (Python 3.11 + FastAPI)
- Builds frontend (Node 18 + React)
- Creates Docker network
- Starts all services in detached mode

**Expected output**:
```
[+] Running 3/3
 ✔ Container microblog-db-1       Started
 ✔ Container microblog-backend-1  Started
 ✔ Container microblog-frontend-1 Started
```

### 4. Run Database Migrations

```bash
docker-compose exec backend alembic upgrade head
```

**Expected output**:
```
INFO  [alembic.runtime.migration] Running upgrade -> a1b2c3d4e5f6, initial schema
INFO  [alembic.runtime.migration] Running upgrade a1b2c3d4e5f6 -> b2c3d4e5f6a1, add indexes
```

### 5. Seed Mock Data (10 Posts)

```bash
docker-compose exec backend python scripts/seed_data.py
```

**Expected output**:
```
🌱 Seeding database...
✅ Created 3 users
✅ Created 5 categories
✅ Created 10 posts (8 published, 2 drafts)
✅ Created 15 comments
✅ Created 42 reactions
✅ Database seeded successfully!
```

### 6. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

**Test credentials** (from seed data):
```
Email: author1@example.com
Password: password123
```

---

## Verify Installation

### Check Services Status

```bash
docker-compose ps
```

Expected output (all services `Up`):
```
NAME                     STATUS              PORTS
microblog-backend-1      Up 30 seconds       0.0.0.0:8000->8000/tcp
microblog-db-1           Up 30 seconds       0.0.0.0:3306->3306/tcp
microblog-frontend-1     Up 30 seconds       0.0.0.0:3000->3000/tcp
```

### Test API Health

```bash
curl http://localhost:8000/health
```

Expected: `{"status":"ok","environment":"development"}`

### Test Homepage

```bash
curl http://localhost:8000/posts | jq
```

Expected: JSON array with 8 published posts (2 drafts excluded)

### Test Frontend

Visit http://localhost:3000 - you should see:
- 3-column layout on desktop (≥1024px width)
- Post previews in center column
- Category list in right sidebar (5 categories)
- Recent posts in left sidebar

---

## Development Workflow

### View Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend

# Database only
docker-compose logs -f db
```

### Restart Services

```bash
# Restart backend (e.g., after code changes)
docker-compose restart backend

# Restart all services
docker-compose restart
```

### Run Tests

```bash
# Run all backend tests
docker-compose exec backend bash scripts/unittest.sh

# Run specific test file
docker-compose exec backend pytest tests/integration/test_posts_router.py -v

# Run with coverage
docker-compose exec backend pytest --cov=src --cov-report=html
```

### Create Database Migration

```bash
# Auto-generate migration from model changes
docker-compose exec backend alembic revision --autogenerate -m "add_field_to_post"

# Edit migration file (if needed)
vim backend/alembic/versions/<migration_id>_add_field_to_post.py

# Apply migration
docker-compose exec backend alembic upgrade head
```

### Access Database

```bash
# MySQL CLI
docker-compose exec db mysql -u bloguser -pblogpass microblog

# Query posts
docker-compose exec db mysql -u bloguser -pblogpass microblog -e "SELECT id, title, status FROM posts;"
```

### Stop Services

```bash
# Stop without removing containers
docker-compose stop

# Stop and remove containers (keeps volumes)
docker-compose down

# Stop and remove everything including volumes (DATA LOSS!)
docker-compose down -v
```

---

## Local Development (Without Docker)

For faster iteration, run backend/frontend natively:

### Backend Setup

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start MySQL (via Docker or local install)
docker run --name microblog-mysql -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=microblog \
  -e MYSQL_USER=bloguser \
  -e MYSQL_PASSWORD=blogpass \
  -d mysql:8.0

# Update .env for localhost
echo "DATABASE_URL=mysql+aiomysql://bloguser:blogpass@localhost:3306/microblog" > .env

# Run migrations
alembic upgrade head

# Seed data
python scripts/seed_data.py

# Start backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Update .env
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Start frontend
npm start
```

Frontend will auto-open at http://localhost:3000

---

## Running Unit Tests (unittest.sh)

The `scripts/unittest.sh` script runs all router tests:

```bash
# Via Docker
docker-compose exec backend bash scripts/unittest.sh

# Local
cd backend
bash scripts/unittest.sh
```

**Script contents** (`backend/scripts/unittest.sh`):
```bash
#!/usr/bin/env bash
set -e

echo "🧪 Running unit tests for API routers..."

# Run integration tests (router tests)
pytest tests/integration/ \
  -v \
  --tb=short \
  --cov=src/api/routers \
  --cov-report=term-missing \
  --cov-report=html:coverage_html

echo ""
echo "✅ All tests passed!"
echo "📊 Coverage report: coverage_html/index.html"
```

**Test execution output**:
```
🧪 Running unit tests for API routers...
tests/integration/test_auth_router.py::test_register_user PASSED
tests/integration/test_auth_router.py::test_login_user PASSED
tests/integration/test_posts_router.py::test_get_posts PASSED
tests/integration/test_posts_router.py::test_create_post PASSED
tests/integration/test_posts_router.py::test_update_post PASSED
tests/integration/test_comments_router.py::test_create_comment PASSED
tests/integration/test_reactions_router.py::test_toggle_reaction PASSED

---------- coverage: platform darwin, python 3.11.6 -----------
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
src/api/routers/auth.py              45      2    96%   23, 67
src/api/routers/posts.py             78      5    94%   112, 145, 178, 201, 234
src/api/routers/comments.py          32      1    97%   89
src/api/routers/reactions.py         28      0   100%
src/api/routers/categories.py        22      1    95%   56
src/api/routers/search.py            18      0   100%
---------------------------------------------------------------
TOTAL                               223      9    96%

✅ All tests passed!
📊 Coverage report: coverage_html/index.html
```

---

## Troubleshooting

### Port Already in Use

If ports 3000, 8000, or 3306 are already in use:

```bash
# Check what's using port 8000
lsof -i :8000

# Kill process (replace PID)
kill -9 <PID>

# Or change port in docker-compose.yml
```

### Database Connection Error

If backend can't connect to MySQL:

```bash
# Check MySQL is running
docker-compose ps db

# Check logs
docker-compose logs db

# Restart MySQL
docker-compose restart db

# Wait 10 seconds for MySQL to be ready, then retry
```

### Migration Conflicts

If Alembic complains about migration conflicts:

```bash
# Check current revision
docker-compose exec backend alembic current

# Downgrade to base
docker-compose exec backend alembic downgrade base

# Re-apply all migrations
docker-compose exec backend alembic upgrade head
```

### Frontend Can't Reach Backend

If frontend shows API errors:

1. Check `frontend/.env` has correct `REACT_APP_API_URL`
2. Check backend is running: `docker-compose ps backend`
3. Test backend directly: `curl http://localhost:8000/posts`
4. Check CORS settings in `backend/src/main.py`

### Seed Data Already Exists

If `seed_data.py` errors with duplicate data:

```bash
# Clear database and re-seed
docker-compose down -v  # WARNING: Deletes all data
docker-compose up -d
docker-compose exec backend alembic upgrade head
docker-compose exec backend python scripts/seed_data.py
```

Or manually check for existing data:
```python
# Modify scripts/seed_data.py to skip if data exists
async def seed():
    db = SessionLocal()
    existing_posts = await db.execute(select(Post))
    if existing_posts.scalars().first():
        print("⚠️  Data already exists, skipping seed")
        return
    # ... rest of seed logic
```

---

## Next Steps

After successful quickstart:

1. **Explore API Docs**: Visit http://localhost:8000/docs to see all endpoints
2. **Test User Flows**:
   - Register new account at http://localhost:3000/register
   - Login with test account
   - Create a blog post
   - Add comments and reactions
3. **Review Architecture**: Read [research.md](research.md) for Clean Architecture details
4. **Review Data Model**: Read [data-model.md](data-model.md) for entity relationships
5. **Review API Contracts**: See [contracts/api.yaml](contracts/api.yaml) for endpoint specifications
6. **Start Development**: See [plan.md](plan.md) for project structure and implementation guidelines

---

## Production Deployment Notes

For production deployment (beyond local development):

1. **Environment Variables**: Change `SECRET_KEY`, `DEBUG=false`, use strong MySQL password
2. **HTTPS**: Configure nginx reverse proxy with SSL/TLS certificates
3. **Database**: Use managed MySQL service (AWS RDS, Google Cloud SQL) or persistent volumes
4. **Migrations**: Run `alembic upgrade head` before deployment
5. **Monitoring**: Add logging, error tracking (Sentry), performance monitoring (APM)
6. **Backup**: Schedule database backups (mysqldump or managed service snapshots)
7. **Security**: Review CORS settings, rate limiting, CSP headers

---

**Quickstart Complete** ✅  
You now have a fully functional personal blog platform running locally!
