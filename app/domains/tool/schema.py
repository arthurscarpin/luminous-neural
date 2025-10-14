from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, Field

# --- Input Schema ---
class ToolCreateSchema(BaseModel):
    """Schema for creating a new Tool."""
    name: Annotated[str, Field(min_length=3, max_length=30, description='Name of the Tool')]
    description: Annotated[str, Field(str, min_length=10, max_length=255, description='Description of the Tool')]
    path: Annotated[str, Field(str, min_length=10, max_length=255, description='Path of the Tool')]
    created_by: Annotated[str, Field(min_length=3, max_length=50, description='User or system that created the Tool')] = "system"

class ToolUpdateSchema(BaseModel):
    """Schema for updating an Tool. All fields optional."""
    name: Optional[Annotated[str, Field(min_length=3, max_length=30, description='Name of the Tool')]] = None
    description: Optional[Annotated[str, Field(min_length=10, max_length=255, description='Description of the Tool')]] = None
    path: Annotated[str, Field(str, min_length=10, max_length=255, description='Path of the Tool')]
    updated_by: Annotated[str, Field(min_length=3, max_length=50, description='User or system that updated the Tool')] = "system"

# --- Output Schema ---
class ToolResponseSchema(BaseModel):
    """Schema representing an Tool for API responses."""
    id: int
    name: str
    description: str
    path: str
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

    model_config = {'from_attributes': True}