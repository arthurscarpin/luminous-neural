from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.sql_database import Base

# --- Table related to IA Group X Agent ---
ia_group_agent_association = Table(
    'ia_group_agent',
    Base.metadata,
    Column('ia_group_id', Integer, ForeignKey('ia_group.id', ondelete='CASCADE'), primary_key=True),
    Column('agent_id', Integer, ForeignKey('agent.id', ondelete='CASCADE'), primary_key=True)
)