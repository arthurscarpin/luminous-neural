from app.domains.mixins.timestamp import TimestampMixin
from app.domains.mixins.audit import AuditMixin
from app.core.sql_database import Base

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class Enterprise(TimestampMixin, AuditMixin, Base):
    """
    Represents an enterprise entity.

    Inherits:
        TimestampMixin: Adds created_at and updated_at timestamps.
        AuditMixin: Adds auditing fields like created_by and updated_by.
        Base: SQLAlchemy declarative base.
    """
    __tablename__ = 'enterprise'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    ia_model: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    def __repr__(self) -> str:
        """Returns a string representation of the Enterprise instance.

        The string includes the id, name, and creation timestamp for easier debugging.

        Returns:
            str: Formatted string representing the Enterprise instance.
        """
        return f'Enterprise({self.id=}, {self.name=}, {self.created_at=})'