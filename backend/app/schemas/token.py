from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    """
    Token schema for authentication response.
    
    Attributes:
        access_token: JWT token string
        token_type: Type of token (always "bearer")
    """
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    """
    Token payload schema for JWT token content.
    
    Attributes:
        sub: User ID (subject)
        role: User role (admin, staff, or member)
    """
    sub: Optional[int] = None 