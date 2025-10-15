from app.domains.mixins.timestamp import TimestampMixin
from app.domains.mixins.audit import AuditMixin
from app.core.sql_database import Base
from app.domains.associations.agent_tool_association import agent_tool_association
from app.domains.associations.enterprise_agent_association import enterprise_agent_association
from app.domains.associations.ia_group_agent_association import ia_group_agent_association

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Agent(TimestampMixin, AuditMixin, Base):
    """
    Represents agents with metadata for auditing and timestamps.

    Inherits:
        TimestampMixin: Provides created_at and updated_at timestamp fields.
        AuditMixin: Provides fields for tracking creation and modification users.
        Base: SQLAlchemy declarative base.
        Relationship: 
            Agent X Tool
            Agent X Enterprise
    """
    __tablename__ = 'agent'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    system_message: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    tools = relationship(
        'Tool',
        secondary=agent_tool_association,
        back_populates='agents'
    )

    enterprises = relationship(
        'Enterprise',
        secondary=enterprise_agent_association,
        back_populates='agents'
    )

    ia_groups = relationship(
        'IAGroup',
        secondary=ia_group_agent_association,
        back_populates='agents'
    )
        
    def __repr__(self) -> str:
        """
        Returns a string representation of the Agent instance.

        Returns:
            str: Formatted string showing id, name, and creation timestamp.
        """
        return f'Agent({self.id=}, {self.name=}, {self.created_at=})'
    