import pytest
from datetime import datetime, timedelta
from jose import jwt
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_token,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

def test_password_hashing():
    """Test password hashing and verification"""
    password = "test_password123"
    hashed_password = get_password_hash(password)
    
    # Verify password matches
    assert verify_password(password, hashed_password) is True
    
    # Verify wrong password doesn't match
    assert verify_password("wrong_password", hashed_password) is False

def test_token_creation():
    """Test JWT token creation"""
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    
    # Verify token structure
    assert isinstance(token, str)
    assert len(token.split(".")) == 3  # JWT has 3 parts
    
    # Verify token contents
    decoded = jwt.decode(token, options={"verify_signature": False})
    assert decoded["sub"] == "test@example.com"
    assert "exp" in decoded
    assert "iat" in decoded

def test_token_verification():
    """Test JWT token verification"""
    # Create a valid token
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    
    # Verify valid token
    payload = verify_token(token)
    assert payload["sub"] == "test@example.com"
    
    # Test invalid token
    with pytest.raises(jwt.JWTError):
        verify_token("invalid.token.string")
    
    # Test expired token
    expired_data = {
        "sub": "test@example.com",
        "exp": datetime.utcnow() - timedelta(minutes=1)
    }
    expired_token = jwt.encode(expired_data, "secret", algorithm=ALGORITHM)
    with pytest.raises(jwt.ExpiredSignatureError):
        verify_token(expired_token)

def test_token_expiration():
    """Test token expiration time"""
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    
    # Decode token without verification
    decoded = jwt.decode(token, options={"verify_signature": False})
    
    # Check expiration time
    exp_timestamp = decoded["exp"]
    iat_timestamp = decoded["iat"]
    assert exp_timestamp - iat_timestamp == ACCESS_TOKEN_EXPIRE_MINUTES * 60

def test_token_payload():
    """Test token payload structure"""
    data = {
        "sub": "test@example.com",
        "role": "admin",
        "extra": "data"
    }
    token = create_access_token(data)
    
    # Verify payload
    payload = verify_token(token)
    assert payload["sub"] == data["sub"]
    assert payload["role"] == data["role"]
    assert payload["extra"] == data["extra"] 