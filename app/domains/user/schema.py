from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

# --- Input Schemas ---
class UserCreateSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Full name of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    password: str = Field(..., min_length=8, max_length=128, description="Password with at least 1 uppercase, 1 lowercase, 1 number")
    is_admin: Optional[bool] = Field(default=False, description="Admin privileges flag")
    created_by: Optional[str] = Field(default="system", description="User or system that created this user")

    @field_validator("password")
    def password_complexity(cls, v: str) -> str:
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        return v

class UserUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50, description="Full name of the user")
    email: Optional[EmailStr] = Field(None, description="Email address of the user")
    password: Optional[str] = Field(None, min_length=8, max_length=128, description="Password with at least 1 uppercase, 1 lowercase, 1 number")
    is_admin: Optional[bool] = None
    status: Optional[bool] = None
    updated_by: Optional[str] = Field(default="system", description="User or system that updated this user")

    @field_validator("password")
    def password_complexity(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        return v

# --- Output Schema ---
class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: str
    is_admin: bool
    status: bool
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

    model_config = {"from_attributes": True}
