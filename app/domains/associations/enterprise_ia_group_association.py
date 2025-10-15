from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.sql_database import Base

# --- Table related to Enterprise X IA Group ---
enterprise_ia_group_association = Table(
    'enterprise_ia_group',
    Base.metadata,
    Column('enterprise_id', Integer, ForeignKey('enterprise.id', ondelete='CASCADE'), primary_key=True),
    Column('ia_group_id', Integer, ForeignKey('ia_group.id', ondelete='CASCADE'), primary_key=True)
)