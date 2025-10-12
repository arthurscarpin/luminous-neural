from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class AuditMixin:
    """Mixin that adds audit information to a model.

    Attributes:
        created_by (Mapped[str]): The username or identifier of the user who created the record.
        updated_by (Mapped[Optional[str]]): The username or identifier of the user who last updated the record, optional.
    """
    created_by: Mapped[str] = mapped_column(String(50), nullable=False)
    updated_by: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    def __repr__(self) -> str:
        """Returns a string representation of the audit information.

        Returns:
            str: Formatted string showing created_by and updated_by values.
        """
        return f'AuditMixin({self.created_by=}, {self.updated_by=})'