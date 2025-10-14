from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, Field

# --- Input Schema ---
class EnterpriseCreateSchema(BaseModel):
    """Schema for creating a new enterprise."""
    name: Annotated[str, Field(min_length=3, max_length=30, description='Name of the enterprise')]
    description: Annotated[str, Field(min_length=10, max_length=255, description='Description of the enterprise')]
    ia_model: Annotated[str, Field(min_length=3, max_length=50, description='AI model associated with the enterprise')]
    created_by: Annotated[str, Field(min_length=3, max_length=50, description='User or system that created the enterprise')] = "system"

class EnterpriseUpdateSchema(BaseModel):
    """Schema for updating an enterprise. All fields optional."""
    name: Optional[Annotated[str, Field(min_length=3, max_length=30, description='Name of the enterprise')]] = None
    description: Optional[Annotated[str, Field(min_length=10, max_length=255, description='Description of the enterprise')]] = None
    ia_model: Optional[Annotated[str, Field(min_length=3, max_length=50, description='AI model associated with the enterprise')]] = None
    updated_by: Annotated[str, Field(min_length=3, max_length=50, description='User or system that updated the enterprise')] = "system"

# --- Output Schema ---
class EnterpriseResponseSchema(BaseModel):
    """Schema representing an enterprise for API responses."""
    id: int
    name: str
    description: str
    ia_model: str
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

    model_config = {'from_attributes': True}
