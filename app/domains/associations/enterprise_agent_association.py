from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.sql_database import Base

# --- Table related to Enterprise X Agent ---
enterprise_agent_association = Table(
    'enterprise_agent',
    Base.metadata,
    Column('enterprise_id', Integer, ForeignKey('enterprise.id', ondelete='CASCADE'), primary_key=True),
    Column('agent_id', Integer, ForeignKey('agent.id', ondelete='CASCADE'), primary_key=True)
)