from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

# --- Input Schemas ---
class EnterpriseCreateSchema(BaseModel):
    """Schema for creating a new Enterprise.

    This schema is used as input for API endpoints that create a new Enterprise.
    It validates the input data to ensure required fields and constraints are met.

    Attributes:
        name (str): Name of the enterprise. Minimum 3 and maximum 30 characters.
        description (str): Description of the enterprise. Minimum 10 and maximum 255 characters.
        ia_model (str): The AI model associated with the enterprise. Minimum 3 and maximum 50 characters.
    """
    name: Annotated[str, Field(..., min_length=3, max_length=30, description='Name of the enterprise')]
    description: Annotated[str, Field(..., min_length=10, max_length=255, description='Description of the enterprise')]
    ia_model: Annotated[str, Field(..., min_length=3, max_length=50, description='AI model associated with the enterprise')]

# --- Output Schemas ---
class EnterpriseResponseSchema(BaseModel):
    """Schema for returning Enterprise data in API responses.

    This schema represents the fields returned by the API when retrieving an Enterprise.
    It is configured with `from_attributes=True` to allow conversion directly from SQLAlchemy models.

    Attributes:
        id (int): Unique identifier of the enterprise.
        name (str): Name of the enterprise.
        description (str): Description of the enterprise.
        ia_model (str): The AI model associated with the enterprise.
        created_at (datetime): Timestamp when the enterprise was created.
        created_by (str): Identifier of the user who created the enterprise.
    """
    id: int
    name: str
    description: str
    ia_model: str
    created_at: datetime
    created_by: str

    model_config = {'from_attributes': True}