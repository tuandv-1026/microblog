"""Unit tests for authentication service."""

import pytest
from src.service.auth_service import auth_service


def test_hash_password():
    """Test password hashing."""
    password = "testpassword123"
    hashed = auth_service.hash_password(password)
    
    assert hashed != password
    assert len(hashed) > 0
    assert hashed.startswith("$2b$")  # bcrypt format


def test_verify_password_correct():
    """Test password verification with correct password."""
    password = "testpassword123"
    hashed = auth_service.hash_password(password)
    
    assert auth_service.verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Test password verification with incorrect password."""
    password = "testpassword123"
    hashed = auth_service.hash_password(password)
    
    assert auth_service.verify_password("wrongpassword", hashed) is False


def test_different_hashes_for_same_password():
    """Test that same password produces different hashes (due to salt)."""
    password = "testpassword123"
    hash1 = auth_service.hash_password(password)
    hash2 = auth_service.hash_password(password)
    
    assert hash1 != hash2
    assert auth_service.verify_password(password, hash1)
    assert auth_service.verify_password(password, hash2)
