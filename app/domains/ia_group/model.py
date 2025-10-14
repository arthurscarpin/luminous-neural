from app.domains.mixins.timestamp import TimestampMixin
from app.domains.mixins.audit import AuditMixin
from app.core.sql_database import Base

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class IAGroup(TimestampMixin, AuditMixin, Base):
    """
    Represents a group of AI agents with metadata for auditing and timestamps.

    Inherits:
        TimestampMixin: Provides created_at and updated_at timestamp fields.
        AuditMixin: Provides fields for tracking creation and modification users.
        Base: SQLAlchemy declarative base.
    """
    __tablename__ = 'ia_group'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
        
    def __repr__(self) -> str:
        """
        Returns a string representation of the IAGroup instance.

        Returns:
            str: Formatted string showing id, name, and creation timestamp.
        """
        return f'IAGroup({self.id=}, {self.name=}, {self.created_at=})'
    