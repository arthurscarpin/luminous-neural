from app.domains.mixins.timestamp import TimestampMixin
from app.domains.mixins.audit import AuditMixin
from app.core.sql_database import Base

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class User(TimestampMixin, AuditMixin, Base):
    """
    Represents Users with metadata for auditing and timestamps.

    Inherits:
        TimestampMixin: Provides created_at and updated_at timestamp fields.
        AuditMixin: Provides fields for tracking creation and modification users.
        Base: SQLAlchemy declarative base.
    """
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
        
    def __repr__(self) -> str:
        """
        Returns a string representation of the User instance.

        Returns:
            str: Formatted string showing id, name, and creation timestamp.
        """
        return f'User({self.id=}, {self.name=}, {self.email}, {self.created_at=})'
    