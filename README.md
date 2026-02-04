# Microblog - Personal Blog Platform

A modern personal blog platform built with FastAPI, React, and MySQL, featuring Markdown support and a clean, responsive design.

## Features

- ✍️ **Markdown Editor**: Write blog posts in Markdown with live preview
- 📂 **Categories**: Organize posts by categories
- 💬 **Comments**: Engage with readers through comments
- 😊 **Emoji Reactions**: Express emotions with 6 reaction types
- 🔍 **Full-text Search**: Find posts quickly
- 🔐 **Authentication**: Secure user registration and login
- 📱 **Responsive Design**: Mobile-first responsive layout
- 🐳 **Docker Support**: Easy deployment with Docker Compose

## Tech Stack

### Backend
- **FastAPI** 0.104+ - Modern Python web framework
- **SQLAlchemy** 2.0+ - Async ORM
- **MySQL** 8.0+ - Database
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **bcrypt** - Password hashing
- **Markdown** + **bleach** - Markdown rendering with XSS protection

### Frontend
- **React** 18 - UI framework
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **react-markdown** - Markdown rendering

### Architecture
- **Clean Architecture** - 5-layer separation (domain, usecase, service, driver, api)
- **Repository Pattern** - Abstract data access
- **Dependency Injection** - FastAPI DI container

## Quick Start

### Prerequisites
- Docker & Docker Compose
- OR: Python 3.11+, Node.js 18+, MySQL 8.0+

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd microblog

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Start all services
docker-compose up -d

# Run database migrations
docker-compose exec backend alembic upgrade head

# Seed database with sample data
docker-compose exec backend python scripts/seed_data.py
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

### Option 2: Local Development

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
alembic upgrade head

# Seed database
python scripts/seed_data.py

# Start server
uvicorn src.api.main:app --reload
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy and configure environment
cp .env.example .env

# Start development server
npm start
```

## Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Testing

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run unit tests only
./scripts/unittest.sh
```

## Project Structure

```
microblog/
├── backend/
│   ├── src/
│   │   ├── domain/          # Domain entities and repository interfaces
│   │   ├── usecase/         # Business logic / use cases
│   │   ├── service/         # External services (markdown, auth)
│   │   ├── driver/          # Database implementation
│   │   └── api/             # FastAPI routes and schemas
│   ├── alembic/             # Database migrations
│   ├── tests/               # Unit and integration tests
│   └── scripts/             # Utility scripts
├── frontend/
│   └── src/
│       ├── components/      # React components
│       ├── pages/           # Page components
│       ├── services/        # API services
│       └── styles/          # CSS styles
└── docker-compose.yml       # Docker orchestration
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user

### Posts
- `GET /api/posts` - Get all posts (with filters)
- `GET /api/posts/{slug}` - Get post by slug
- `POST /api/posts` - Create post (auth required)
- `PATCH /api/posts/{id}` - Update post (auth required)
- `POST /api/posts/{id}/publish` - Publish post (auth required)
- `DELETE /api/posts/{id}` - Delete post (auth required)

### Categories
- `GET /api/categories` - Get all categories
- `GET /api/categories/{slug}` - Get category by slug

### Comments
- `POST /api/comments` - Create comment
- `GET /api/comments/post/{post_id}` - Get post comments

### Reactions
- `POST /api/reactions` - Toggle reaction (auth required)
- `GET /api/reactions/post/{post_id}/summary` - Get reaction counts

### Search
- `GET /api/search?q=query` - Search posts

### About
- `GET /api/about` - Get about page

## Default Credentials

After seeding the database:
- **Username**: admin
- **Password**: admin123

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
