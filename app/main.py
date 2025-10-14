from app.domains.enterprise.controller import enterprise_router
from app.domains.ia_group.controller import ia_group_router
from app.domains.agent.controller import agent_router
from app.domains.tool.controller import tool_router
from app.domains.user.controller import user_router
from app.api.exception_handlers import register_exception_handlers

from fastapi import FastAPI

app = FastAPI(
    title='Luminous Neural', 
    description='Luminous Neural is a system of collaborative AI agents that learn, reason, and evolve together.',
    version='0.1.0'
)

# --- HTTP Routes ---
app.include_router(enterprise_router)
app.include_router(ia_group_router)
app.include_router(agent_router)
app.include_router(tool_router)
app.include_router(user_router)

# --- Exception Handlers ---
register_exception_handlers(app)