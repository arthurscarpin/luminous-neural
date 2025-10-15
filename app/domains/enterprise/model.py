from app.domains.mixins.timestamp import TimestampMixin
from app.domains.mixins.audit import AuditMixin
from app.core.sql_database import Base
from app.domains.associations.enterprise_agent_association import enterprise_agent_association
from app.domains.associations.enterprise_ia_group_association import enterprise_ia_group_association
from app.domains.associations.enterprise_user_association import enterprise_user_association

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Enterprise(TimestampMixin, AuditMixin, Base):
    """
    Represents an enterprise entity.

    Inherits:
        TimestampMixin: Adds created_at and updated_at timestamps.
        AuditMixin: Adds auditing fields like created_by and updated_by.
        Base: SQLAlchemy declarative base.
        Relationship: 
            Enterprise X Agent
            Enterprise X IA Group
    """
    __tablename__ = 'enterprise'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    ia_model: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    agents = relationship(
        'Agent',
        secondary=enterprise_agent_association,
        back_populates='enterprises'
    )

    ia_groups = relationship(
        'IAGroup',
        secondary=enterprise_ia_group_association,
        back_populates='enterprises'
    )

    users = relationship(
        'User',
        secondary=enterprise_user_association,
        back_populates='enterprises'
    )
    
    def __repr__(self) -> str:
        """Returns a string representation of the Enterprise instance.

        The string includes the id, name, and creation timestamp for easier debugging.

        Returns:
            str: Formatted string representing the Enterprise instance.
        """
        return f'Enterprise({self.id=}, {self.name=}, {self.created_at=})'