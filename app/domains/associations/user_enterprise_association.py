from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.sql_database import Base

# --- Table related to Enterprise X User ---
user_enterprise_association = Table(
    'user_enterprise',
    Base.metadata,
    Column('enterprise_id', Integer, ForeignKey('enterprise.id', ondelete='CASCADE'), primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
)