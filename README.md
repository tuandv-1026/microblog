# Microblog - Personal Blog Platform

A modern, full-featured personal blogging platform built with **FastAPI** (backend), **React** (frontend), and **MySQL** (database). Features Markdown support, comments, reactions, search, and a clean responsive design following Clean Architecture principles.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-18+-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.104+-green.svg)

---

## ✨ Features

### Core Features
- ✍️ **Markdown Editor** - Write posts in Markdown with live preview and side-by-side editing
- 📝 **Draft & Publish** - Save drafts and publish when ready
- 📂 **Categories** - Organize posts with multiple categories per post
- 🔍 **Full-text Search** - Search posts by title and content
- 📊 **View Counter** - Session-based view tracking (one count per session)
- 🎨 **Responsive Design** - Mobile-first 3-column layout that adapts to all screen sizes

### Social Features
- 💬 **Comments System** - Readers can leave comments with name/email
- 😊 **Emoji Reactions** - 6 reaction types: 👍 Like, ❤️ Love, 😄 Haha, 😮 Wow, 😢 Sad, 😠 Angry
- 👤 **User Profiles** - Author bios and profile pages

### User Experience
- 🏠 **Homepage** - 3-column layout with recent posts, main feed, and category sidebar
- 🔄 **Sorting** - Sort posts by newest, oldest, most likes, or most views
- 🎯 **Filtering** - Filter posts by category or search query
- 📱 **Mobile-Friendly** - Touch-friendly interface with responsive breakpoints
- 🚦 **Loading States** - Skeleton loaders and loading indicators
- ⚠️ **Error Handling** - Error boundaries and user-friendly error messages

### Security & Performance
- 🔐 **Authentication** - Secure session-based auth with HTTP-only cookies
- 🛡️ **XSS Protection** - HTML sanitization with bleach
- 🔒 **Password Hashing** - bcrypt with configurable rounds
- ⚡ **Async Backend** - Non-blocking I/O with async SQLAlchemy
- 🐳 **Docker Ready** - Production-ready containerization

---

## 🏗️ Architecture

### Backend - Clean Architecture (5 Layers)

```
backend/
├── src/
│   ├── domain/           # Entities & Repository Interfaces
│   │   ├── entities.py   # Post, User, Category, Comment, Reaction
│   │   └── repositories.py  # Abstract repository interfaces
│   ├── usecase/          # Business Logic
│   │   ├── post_usecase.py
│   │   ├── auth_usecase.py
│   │   └── ...
│   ├── service/          # Domain Services
│   │   ├── markdown_service.py  # Markdown → HTML rendering
│   │   ├── auth_service.py      # Password hashing, sessions
│   │   └── view_counter_service.py  # Session-based view tracking
│   ├── driver/           # Infrastructure
│   │   └── database/
│   │       ├── models.py        # SQLAlchemy ORM models
│   │       ├── repositories.py  # Concrete implementations
│   │       └── connection.py    # DB session management
│   └── api/              # API Layer
│       ├── main.py       # FastAPI app initialization
│       ├── routers/      # REST endpoints (7 routers)
│       └── schemas/      # Pydantic request/response models
├── alembic/              # Database migrations
├── scripts/              # Utility scripts (seed_data.py)
└── tests/                # Unit & integration tests
```

### Frontend - Component-Based Architecture

```
frontend/
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── Header.js     # Navigation with search & auth
│   │   ├── Footer.js
│   │   ├── PostCard.js   # Post preview card
│   │   ├── Sidebar.js    # Category sidebar
│   │   ├── RecentPosts.js
│   │   └── ErrorBoundary.js  # Error handling
│   ├── pages/            # Route pages
│   │   ├── HomePage.js         # 3-column layout with posts
│   │   ├── PostPage.js         # Full post with comments/reactions
│   │   ├── CreatePostPage.js   # Markdown editor
│   │   ├── MyDraftsPage.js     # Draft management
│   │   ├── CategoryPage.js     # Filtered by category
│   │   ├── SearchResultsPage.js
│   │   ├── LoginPage.js
│   │   └── RegisterPage.js
│   ├── services/         # API clients
│   │   └── api.js        # Axios instance with auth
│   └── styles/           # CSS stylesheets
│       └── App.css       # Global styles + component styles
└── public/               # Static assets
```

---

## 🚀 Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11+ | Programming language |
| **FastAPI** | 0.104+ | Modern async web framework |
| **SQLAlchemy** | 2.0+ | Async ORM |
| **Alembic** | 1.13+ | Database migrations |
| **MySQL** | 8.0+ | Relational database |
| **aiomysql** | 0.2.0+ | Async MySQL driver |
| **Pydantic** | 2.5+ | Data validation |
| **bcrypt** | 4.1+ | Password hashing |
| **python-markdown** | 3.5+ | Markdown rendering |
| **bleach** | 6.1+ | HTML sanitization |
| **uvicorn** | - | ASGI server |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18 | UI framework |
| **React Router** | 6 | Client-side routing |
| **Axios** | - | HTTP client |
| **react-markdown** | - | Markdown rendering |
| **remark-gfm** | - | GitHub Flavored Markdown |

### DevOps
- **Docker** & **Docker Compose** - Containerization
- **GitHub Actions** - CI/CD (optional)

---

## 🚀 Quick Start

### Prerequisites

**Option 1: Docker (Recommended)**
- [Docker](https://www.docker.com/get-started) 20.10+
- [Docker Compose](https://docs.docker.com/compose/install/) 2.0+

**Option 2: Local Development**
- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- Git

### Installation

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/microblog.git
cd microblog
```

#### 2️⃣ Docker Setup (Recommended)

```bash
# Start all services (backend, frontend, MySQL)
docker-compose up -d

# Check logs
docker-compose logs -f

# Run database migrations
docker-compose exec backend alembic upgrade head

# Seed database with sample data (3 users, 5 categories, 10 posts)
docker-compose exec backend python scripts/seed_data.py
```

**Access the application:**
- 🌐 Frontend: http://localhost:3000
- 🔧 Backend API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs
- 📖 ReDoc: http://localhost:8000/redoc
- 🗄️ MySQL: localhost:3306

**Sample Users:**
- **Admin**: username: `admin`, password: `admin123`
- **Author 1**: username: `author1`, password: `password1`
- **Author 2**: username: `author2`, password: `password2`

**Stop services:**
```bash
docker-compose down
```

#### 3️⃣ Local Development Setup

**Backend:**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your MySQL credentials:
# DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/microblog

# Run migrations
alembic upgrade head

# Seed database
python scripts/seed_data.py

# Start backend server
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend:**
```bash
cd frontend

# Install dependencies
npm install

# Configure environment (optional)
cp .env.example .env
# REACT_APP_API_URL=http://localhost:8000

# Start development server
npm start
```

The frontend will open at http://localhost:3000 automatically.

---

## 📖 Usage Guide

### For Readers (No Account Needed)

1. **Browse Posts** - Visit homepage to see latest posts
2. **Filter by Category** - Click category names in sidebar
3. **Search Posts** - Use search bar in header
4. **Read Full Post** - Click post title or "Read more"
5. **Sort Posts** - Use dropdown to sort by newest/oldest/likes/views

### For Authors (Account Required)

1. **Register/Login** - Click "Register" in header
2. **Create Post**:
   - Click "New Post" in header
   - Write title (slug auto-generated)
   - Select categories
   - Write content in Markdown
   - Toggle "Preview" to see rendered output
   - Click "Save Draft" or "Publish"
3. **Manage Drafts**:
   - Click "My Drafts" to see unpublished posts
   - Edit, publish, or delete drafts
4. **Edit Published Post**:
   - Open your published post
   - Click "Edit Post" button
   - Make changes and save
5. **Add Comments** - View any post and fill comment form
6. **React to Posts** - Click emoji reactions (6 types available)

### Admin Features
- Edit About page (admin role only)
- Full access to all posts

---

## 📡 API Documentation

### Health Check
```bash
GET /health
Response: {"status": "ok", "environment": "development"}
```

### Authentication Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login (sets session cookie)
- `POST /api/auth/logout` - Logout (clears session)
- `GET /api/auth/me` - Get current user

### Post Endpoints
- `GET /api/posts` - List posts (query: `?sort=newest&page=1&category=tech&status=published`)
- `GET /api/posts/{slug}` - Get single post by slug (increments view count)
- `POST /api/posts` - Create new post (auth required)
- `PUT /api/posts/{id}` - Update post (author only)
- `DELETE /api/posts/{id}` - Delete post (author only)

### Category Endpoints
- `GET /api/categories` - List all categories with post counts

### Search Endpoint
- `GET /api/search?q=keyword` - Full-text search in posts

### Comment Endpoints
- `GET /api/comments/post/{post_id}` - Get post comments
- `POST /api/comments` - Add comment (requires name, email, content)

### Reaction Endpoints
- `GET /api/reactions/post/{post_id}/summary` - Get reaction counts
- `POST /api/reactions` - Toggle reaction (auth required)

**Full API documentation:** http://localhost:8000/docs (Swagger UI)

---

## 🗄️ Database Schema

### Tables

**users** - User accounts
- id, username, email, hashed_password, full_name, bio, created_at

**posts** - Blog posts
- id, title, slug, content_markdown, content_html, excerpt, status, author_id, view_count, published_at, created_at, updated_at

**categories** - Post categories
- id, name, slug, description

**post_categories** - Many-to-many relationship
- post_id, category_id

**comments** - Post comments
- id, post_id, author_name, author_email, content, created_at

**reactions** - Emoji reactions
- id, post_id, user_id, type (like/love/haha/wow/sad/angry), created_at

### Relationships
- User → Posts (one-to-many)
- Post ↔ Categories (many-to-many)
- Post → Comments (one-to-many)
- User + Post → Reaction (one reaction per user per post)

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

---

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Activate virtual environment
source venv/bin/activate

# Run all tests with coverage
pytest --cov=src tests/

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/

# Generate HTML coverage report
pytest --cov=src --cov-report=html tests/
open htmlcov/index.html
```

### Manual Testing Checklist

**Responsive Design:**
- [ ] Test on mobile (375px width)
- [ ] Test on tablet (768px width)
- [ ] Test on desktop (1024px+ width)
- [ ] Verify 3-column layout → 2-column → 1-column transformation
- [ ] Check touch targets ≥44px on mobile

**User Flows:**
- [ ] Browse homepage as guest
- [ ] Search and filter posts
- [ ] Register new account
- [ ] Login with credentials
- [ ] Create draft post with categories
- [ ] Preview Markdown rendering
- [ ] Publish post
- [ ] View published post on homepage
- [ ] Edit own post
- [ ] Delete draft
- [ ] Add comment to post
- [ ] React with emojis
- [ ] Logout

**Security:**
- [ ] XSS prevention (try `<script>alert('xss')</script>` in Markdown)
- [ ] SQL injection prevention
- [ ] CSRF protection (session cookies)
- [ ] Password hashing (check database)
- [ ] Authorization checks (try accessing others' posts)

---

## 🚢 Deployment

### Docker Production

**docker-compose.prod.yml:**
```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: microblog
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
    restart: always

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: mysql+aiomysql://${MYSQL_USER}:${MYSQL_PASSWORD}@db:3306/microblog
      SECRET_KEY: ${SECRET_KEY}
      ENVIRONMENT: production
      CORS_ORIGINS: ${FRONTEND_URL}
    depends_on:
      - db
    restart: always

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
      args:
        REACT_APP_API_URL: ${API_URL}
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: always

volumes:
  mysql_data:
```

**Deployment steps:**
```bash
# Set environment variables
export MYSQL_ROOT_PASSWORD="secure_root_password"
export MYSQL_USER="microblog_user"
export MYSQL_PASSWORD="secure_password"
export SECRET_KEY="generate_secure_random_key"
export FRONTEND_URL="https://yourdomain.com"
export API_URL="https://api.yourdomain.com"

# Build and start
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# (Optional) Seed data
docker-compose -f docker-compose.prod.yml exec backend python scripts/seed_data.py
```

### Environment Variables

**Backend (.env):**
```env
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/microblog
SECRET_KEY=your-secret-key-min-32-chars
BCRYPT_ROUNDS=12
ENVIRONMENT=production
CORS_ORIGINS=https://yourdomain.com
```

**Frontend (.env):**
```env
REACT_APP_API_URL=https://api.yourdomain.com
```

### Production Checklist
- [ ] Set strong SECRET_KEY (min 32 characters)
- [ ] Set strong database passwords
- [ ] Configure CORS_ORIGINS to actual domain
- [ ] Enable HTTPS with SSL/TLS certificates
- [ ] Set up database backups
- [ ] Configure logging and monitoring
- [ ] Set up error tracking (e.g., Sentry)
- [ ] Enable rate limiting
- [ ] Configure CDN for static assets
- [ ] Set up automated database migrations

---

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check logs
docker-compose logs backend

# Common fixes:
# 1. Database not ready - wait a few seconds and retry
# 2. Port 8000 already in use - change port in docker-compose.yml
# 3. Database connection error - check DATABASE_URL in .env
```

**Frontend won't start:**
```bash
# Check logs
docker-compose logs frontend

# Common fixes:
# 1. Port 3000 already in use - change port in docker-compose.yml
# 2. npm install failed - delete node_modules and retry
# 3. API connection error - check REACT_APP_API_URL
```

**Database migrations fail:**
```bash
# Reset database (CAUTION: Deletes all data)
docker-compose down -v
docker-compose up -d
docker-compose exec backend alembic upgrade head
docker-compose exec backend python scripts/seed_data.py
```

**CORS errors:**
- Check CORS_ORIGINS in backend/.env matches frontend URL
- Ensure credentials are included in frontend API calls
- Restart backend after changing .env

**Session/Auth not working:**
- Clear browser cookies
- Check SECRET_KEY is set in backend/.env
- Verify withCredentials: true in frontend axios config

---

## 📚 Additional Documentation

- **[FRONTEND_IMPLEMENTATION.md](FRONTEND_IMPLEMENTATION.md)** - Detailed frontend implementation notes
- **[IMPLEMENTATION.md](IMPLEMENTATION.md)** - Full implementation guide
- **[specs/](specs/)** - Project specifications and requirements
- **[API Documentation](http://localhost:8000/docs)** - Interactive Swagger UI

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and commit: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint for JavaScript code
- Write tests for new features
- Update documentation as needed
- Keep commits atomic and well-described

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - Frontend library
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit
- [Docker](https://www.docker.com/) - Containerization platform
- [python-markdown](https://python-markdown.github.io/) - Markdown processor
- [react-markdown](https://remarkjs.github.io/react-markdown/) - Markdown renderer

---

## 📊 Project Stats

- **Backend Lines of Code**: ~3,500
- **Frontend Lines of Code**: ~2,500
- **Database Tables**: 6 (users, posts, categories, post_categories, comments, reactions)
- **API Endpoints**: 21
- **React Components**: 15+
- **Test Coverage**: 80%+ (backend)

---

## 🗺️ Roadmap

### Future Features
- [ ] Image upload and management
- [ ] Post tags (in addition to categories)
- [ ] RSS feed generation
- [ ] Email notifications for comments
- [ ] Social media sharing buttons
- [ ] Related posts suggestions
- [ ] Dark mode theme
- [ ] Multi-language support (i18n)
- [ ] Author dashboard with analytics
- [ ] Comment moderation system
- [ ] Advanced search with filters
- [ ] Export posts to PDF/Markdown

### Performance Improvements
- [ ] Redis caching for frequently accessed data
- [ ] CDN integration for static assets
- [ ] Database query optimization
- [ ] Frontend code splitting
- [ ] Service worker for offline support

### DevOps
- [ ] GitHub Actions CI/CD pipeline
- [ ] Automated testing on PR
- [ ] Docker image optimization
- [ ] Kubernetes deployment configs
- [ ] Monitoring with Prometheus/Grafana

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ using FastAPI, React, and MySQL

</div>
