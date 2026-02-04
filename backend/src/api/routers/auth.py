"""Authentication router for user registration and login."""

from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.api.schemas import UserCreate, UserResponse, LoginRequest, LoginResponse
from src.driver.database.connection import get_db
from src.driver.database.repositories import SQLAlchemyUserRepository
from src.usecase.auth_usecase import RegisterUserUseCase, LoginUserUseCase

router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user."""
    user_repo = SQLAlchemyUserRepository(db)
    use_case = RegisterUserUseCase(user_repo)
    
    try:
        user = await use_case.execute(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            bio=user_data.bio,
        )
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=LoginResponse)
async def login(
    credentials: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    """Login a user and set session cookie."""
    user_repo = SQLAlchemyUserRepository(db)
    use_case = LoginUserUseCase(user_repo)
    
    try:
        user = await use_case.execute(
            username=credentials.username,
            password=credentials.password,
        )
        
        # Set HTTP-only cookie for session (simplified - should use proper JWT or session)
        response.set_cookie(
            key="session_user_id",
            value=str(user.id),
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=86400,  # 24 hours
        )
        
        return LoginResponse(
            user=UserResponse.model_validate(user),
            message="Login successful",
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout")
async def logout(response: Response):
    """Logout a user by clearing the session cookie."""
    response.delete_cookie("session_user_id")
    return {"message": "Logout successful"}


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    session_user_id: Optional[str] = Cookie(None),
    db: AsyncSession = Depends(get_db),
):
    """Get current authenticated user."""
    if not session_user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        user_id = int(session_user_id)
        user_repo = SQLAlchemyUserRepository(db)
        user = await user_repo.get_by_id(user_id)
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return UserResponse.model_validate(user)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid session")
