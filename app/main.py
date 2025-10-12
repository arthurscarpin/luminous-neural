from fastapi import FastAPI
from app.domains.enterprise.controller import enterprise_routers
from app.api.exception_handlers import register_exception_handlers

app = FastAPI(
    title='Luminous Neural', 
    description='Luminous Neural is a system of collaborative AI agents that learn, reason, and evolve together.',
    version='0.1.0'
)

app.include_router(enterprise_routers)
register_exception_handlers(app)