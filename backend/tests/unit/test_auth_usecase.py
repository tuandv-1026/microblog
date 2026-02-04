"""Unit tests for authentication use cases."""

import pytest
from src.usecase.auth_usecase import RegisterUserUseCase, LoginUserUseCase
from src.domain.entities import User
from src.service.auth_service import auth_service


class MockUserRepository:
    """Mock user repository for testing."""
    
    def __init__(self):
        self.users = {}
        self.next_id = 1
    
    async def create(self, user: User) -> User:
        user.id = self.next_id
        self.next_id += 1
        self.users[user.id] = user
        return user
    
    async def get_by_username(self, username: str):
        for user in self.users.values():
            if user.username == username:
                return user
        return None
    
    async def get_by_email(self, email: str):
        for user in self.users.values():
            if user.email == email:
                return user
        return None


@pytest.mark.asyncio
async def test_register_user_success():
    """Test successful user registration."""
    repo = MockUserRepository()
    use_case = RegisterUserUseCase(repo)
    
    user = await use_case.execute(
        username="testuser",
        email="test@example.com",
        password="password123",
        full_name="Test User",
    )
    
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert auth_service.verify_password("password123", user.hashed_password)


@pytest.mark.asyncio
async def test_register_user_duplicate_username():
    """Test registration with duplicate username."""
    repo = MockUserRepository()
    use_case = RegisterUserUseCase(repo)
    
    # Create first user
    await use_case.execute(
        username="testuser",
        email="test1@example.com",
        password="password123",
    )
    
    # Try to create user with same username
    with pytest.raises(ValueError, match="Username already exists"):
        await use_case.execute(
            username="testuser",
            email="test2@example.com",
            password="password123",
        )


@pytest.mark.asyncio
async def test_login_user_success():
    """Test successful user login."""
    repo = MockUserRepository()
    register_use_case = RegisterUserUseCase(repo)
    login_use_case = LoginUserUseCase(repo)
    
    # Register user
    await register_use_case.execute(
        username="testuser",
        email="test@example.com",
        password="password123",
    )
    
    # Login
    user = await login_use_case.execute("testuser", "password123")
    
    assert user is not None
    assert user.username == "testuser"


@pytest.mark.asyncio
async def test_login_user_invalid_password():
    """Test login with invalid password."""
    repo = MockUserRepository()
    register_use_case = RegisterUserUseCase(repo)
    login_use_case = LoginUserUseCase(repo)
    
    # Register user
    await register_use_case.execute(
        username="testuser",
        email="test@example.com",
        password="password123",
    )
    
    # Try to login with wrong password
    with pytest.raises(ValueError, match="Invalid username or password"):
        await login_use_case.execute("testuser", "wrongpassword")
