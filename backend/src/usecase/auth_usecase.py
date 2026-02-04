"""Use cases for authentication operations."""

from typing import Optional
from src.domain.entities import User
from src.domain.repositories import UserRepository
from src.service.auth_service import auth_service


class RegisterUserUseCase:
    """Use case for user registration."""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def execute(
        self,
        username: str,
        email: str,
        password: str,
        full_name: Optional[str] = None,
        bio: Optional[str] = None,
    ) -> User:
        """
        Register a new user.
        
        Raises:
            ValueError: If username or email already exists
        """
        # Check if username exists
        existing_user = await self.user_repository.get_by_username(username)
        if existing_user:
            raise ValueError("Username already exists")
        
        # Check if email exists
        existing_email = await self.user_repository.get_by_email(email)
        if existing_email:
            raise ValueError("Email already exists")
        
        # Hash password
        hashed_password = auth_service.hash_password(password)
        
        # Create user entity
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            bio=bio,
        )
        
        # Save to database
        return await self.user_repository.create(user)


class LoginUserUseCase:
    """Use case for user login."""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def execute(self, username: str, password: str) -> User:
        """
        Authenticate a user.
        
        Raises:
            ValueError: If credentials are invalid
        """
        # Get user by username
        user = await self.user_repository.get_by_username(username)
        if not user:
            raise ValueError("Invalid username or password")
        
        # Verify password
        if not auth_service.verify_password(password, user.hashed_password):
            raise ValueError("Invalid username or password")
        
        return user
