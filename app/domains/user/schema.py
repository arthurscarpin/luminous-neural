from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, Field, EmailStr

# --- Input Schema ---
class UserCreateSchema(BaseModel):
    """Schema for creating a new User."""
    name: Annotated[str, Field(min_length=3, max_length=50, description='Full name of the user')]
    email: Annotated[EmailStr, Field(description='Email address of the user')]
    password: Annotated[str, Field(min_length=6, max_length=128, description='User password')]
    is_admin: Optional[bool] = Field(default=False, description='Admin privileges flag')
    created_by: Optional[str] = Field(default='system', description='User or system that created this user')

class UserUpdateSchema(BaseModel):
    """Schema for updating an existing User. All fields optional."""
    name: Optional[Annotated[str, Field(min_length=3, max_length=50, description='Full name of the user')]] = None
    email: Optional[Annotated[EmailStr, Field(description='Email address of the user')]] = None
    password: Optional[Annotated[str, Field(min_length=6, max_length=128, description='User password')]] = None
    is_admin: Optional[bool] = None
    status: Optional[bool] = None
    updated_by: Optional[str] = Field(default='system', description='User or system that updated this user')

# --- Output Schema ---
class UserResponseSchema(BaseModel):
    """Schema representing a User for API responses."""
    id: int
    name: str
    email: str
    is_admin: bool
    status: bool
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

    model_config = {'from_attributes': True}
