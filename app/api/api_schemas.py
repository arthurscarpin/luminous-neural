from typing import Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from typing import Generic, TypeVar

T = TypeVar('T')


# --- Success Response ---
class ResponseSchema(GenericModel, Generic[T]):
    """
    Standardized schema for successful API responses.

    Attributes:
        status (str): Indicates the response status. Always set to `'success'`.
        timestamp (datetime): The UTC timestamp of when the response was created.
        data (T): The response payload containing the requested resource or result.
    """

    status: str = 'success'
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    data: T


# --- Error Response ---
class ErrorSchema(BaseModel):
    """
    Standardized schema for error responses.

    Attributes:
        status (str): Indicates the response status. Always set to `'error'`.
        timestamp (datetime): The UTC timestamp of when the error occurred.
        message (str): A short human-readable description of the error.
        details (Optional[str]): Additional technical or contextual details (optional).
    """

    status: str = 'error'
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    message: str
    details: Optional[List[Any]] = None

    model_config = {'json_encoders': {datetime: lambda v: v.isoformat()}}