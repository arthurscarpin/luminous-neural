from typing import Optional

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

class TimestampMixin:
    """Mixin that adds timestamp information to a model.

    Attributes:
        created_at (Mapped[DateTime]): The datetime when the record was created. Defaults to current time.
        updated_at (Mapped[Optional[DateTime]]): The datetime when the record was last updated. Automatically set on update, optional.
    """
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime, nullable=True, onupdate=func.now())

    def __repr__(self) -> str:
        """Returns a string representation of the timestamp information.

        Returns:
            str: Formatted string showing created_at and updated_at values.
        """
        return f'TimestampMixin({self.created_at=}, {self.updated_at=})'