from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field

# --- Input Schema ---
class EnterpriseCreateSchema(BaseModel):
    """
    Schema for creating a new enterprise.

    Attributes:
        name (str): Name of the enterprise (3-30 characters).
        description (str): Description of the enterprise (10-255 characters).
        ia_model (str): AI model associated with the enterprise (3-50 characters).
    """
    name: Annotated[str, Field(..., min_length=3, max_length=30, description='Name of the enterprise')]
    description: Annotated[str, Field(..., min_length=10, max_length=255, description='Description of the enterprise')]
    ia_model: Annotated[str, Field(..., min_length=3, max_length=50, description='AI model associated with the enterprise')]
    created_by: Annotated[str, Field(..., min_length=3, max_length=50, description='User or system that created the enterprise')]

class EnterpriseUpdateSchema(BaseModel):
    """
    Schema for update enterprise.

    Attributes:
        name (str): Name of the enterprise (3-30 characters).
        description (str): Description of the enterprise (10-255 characters).
        ia_model (str): AI model associated with the enterprise (3-50 characters).
    """
    name: Annotated[str, Field(..., min_length=3, max_length=30, description='Name of the enterprise')]
    description: Annotated[str, Field(..., min_length=10, max_length=255, description='Description of the enterprise')]
    ia_model: Annotated[str, Field(..., min_length=3, max_length=50, description='AI model associated with the enterprise')]
    updated_by: Annotated[str, Field(..., min_length=3, max_length=50, description='User or system that updated the enterprise')]

# --- Output Schema ---
class EnterpriseResponseSchema(BaseModel):
    """
    Schema representing an enterprise for API responses.

    Attributes:
        id (int): Unique identifier of the enterprise.
        name (str): Name of the enterprise.
        description (str): Description of the enterprise.
        ia_model (str): AI model associated with the enterprise.
        created_at (datetime): Timestamp when the enterprise was created.
        created_by (str): User who created the enterprise.
    """
    id: int
    name: str
    description: str
    ia_model: str
    created_at: datetime
    created_by: str

    model_config = {'from_attributes': True}

class EnterpriseResponseUpdateSchema(BaseModel):
    """
    Schema representing an enterprise for API responses.

    Attributes:
        id (int): Unique identifier of the enterprise.
        name (str): Name of the enterprise.
        description (str): Description of the enterprise.
        ia_model (str): AI model associated with the enterprise.
        created_at (datetime): Timestamp when the enterprise was created.
        created_by (str): User who created the enterprise.
    """
    id: int
    name: str
    description: str
    ia_model: str
    updated_at: datetime
    updated_by: str

    model_config = {'from_attributes': True}
