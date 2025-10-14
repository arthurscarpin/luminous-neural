from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, Field

# --- Input Schema ---
class AgentCreateSchema(BaseModel):
    """Schema for creating a new Agent."""
    name: Annotated[str, Field(min_length=3, max_length=30, description='Name of the agent')]
    description: Annotated[str, Field(str, min_length=10, max_length=255, description='Description of the agent')]
    system_message: Annotated[str, Field(str, min_length=10, max_length=255, description='System Message of the agent')]
    created_by: Annotated[str, Field(min_length=3, max_length=50, description='User or system that created the agent')] = "system"

class AgentUpdateSchema(BaseModel):
    """Schema for updating an Agent. All fields optional."""
    name: Optional[Annotated[str, Field(min_length=3, max_length=30, description='Name of the agent')]] = None
    description: Optional[Annotated[str, Field(min_length=10, max_length=255, description='Description of the agent')]] = None
    system_message: Annotated[str, Field(str, min_length=10, max_length=255, description='System Message of the agent')]
    updated_by: Annotated[str, Field(min_length=3, max_length=50, description='User or system that updated the agent')] = "system"

# --- Output Schema ---
class AgentResponseSchema(BaseModel):
    """Schema representing an Agent for API responses."""
    id: int
    name: str
    description: str
    system_message: str
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

    model_config = {'from_attributes': True}