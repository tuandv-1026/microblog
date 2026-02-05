"""FastAPI application initialization and configuration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Microblog API",
    description="Personal blog platform with Markdown support",
    version="1.0.0",
    docs_url="/api/docs" if os.getenv("ENVIRONMENT") == "development" else None,
    redoc_url="/api/redoc" if os.getenv("ENVIRONMENT") == "development" else None,
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for production
if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"],  # Configure appropriately for production
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Microblog API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    environment = os.getenv("ENVIRONMENT", "development")
    return {
        "status": "ok",
        "environment": environment,
    }


# Import and include routers
from src.api.routers import auth, posts, categories, comments, reactions, search, about

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(posts.router, prefix="/api/posts", tags=["Posts"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(comments.router, prefix="/api/comments", tags=["Comments"])
app.include_router(reactions.router, prefix="/api/reactions", tags=["Reactions"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(about.router, prefix="/api/about", tags=["About"])
