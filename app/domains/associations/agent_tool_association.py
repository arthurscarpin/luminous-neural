from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.sql_database import Base

# --- Table related to Agent X Tool ---
agent_tool_association = Table(
    'agent_tool',
    Base.metadata,
    Column('agent_id', Integer, ForeignKey('agent.id', ondelete='CASCADE', primary_key=True)),
    Column("tool_id", Integer, ForeignKey("tool.id", ondelete="CASCADE"), primary_key=True)
)