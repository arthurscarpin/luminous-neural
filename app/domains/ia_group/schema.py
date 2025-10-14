from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, Field

# --- Input Schema ---
class IAGroupCreateSchema(BaseModel):
    """Schema for creating a new IA Group."""
    name: Annotated[str, Field(min_length=3, max_length=30, description='Name of the ia_group')]
    description: Annotated[str, Field(str, min_length=10, max_length=255, description='Description of the ia_group')]
    created_by: Annotated[str, Field(min_length=3, max_length=50, description='User or system that created the ia_group')] = "system"

class IAGroupUpdateSchema(BaseModel):
    """Schema for updating an IA Groups. All fields optional."""
    name: Optional[Annotated[str, Field(min_length=3, max_length=30, description='Name of the ia_group')]] = None
    description: Optional[Annotated[str, Field(min_length=10, max_length=255, description='Description of the ia_group')]] = None
    updated_by: Annotated[str, Field(min_length=3, max_length=50, description='User or system that updated the ia_group')] = "system"

# --- Output Schema ---
class IAGroupResponseSchema(BaseModel):
    """Schema representing an IA Group for API responses."""
    id: int
    name: str
    description: str
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

    model_config = {'from_attributes': True}