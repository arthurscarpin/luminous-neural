from app.domains.enterprise.controller import enterprise_router
from app.domains.ia_group.controller import ia_group_router
from app.domains.agent.controller import agent_router
from app.api.exception_handlers import register_exception_handlers

from fastapi import FastAPI

app = FastAPI(
    title='Luminous Neural', 
    description='Luminous Neural is a system of collaborative AI agents that learn, reason, and evolve together.',
    version='0.1.0'
)

app.include_router(enterprise_router)
app.include_router(ia_group_router)
app.include_router(agent_router)
register_exception_handlers(app)