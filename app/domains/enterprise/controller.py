from fastapi import APIRouter

enterprise_routers = APIRouter()

@enterprise_routers.post('/enterprise')
def create_enterprise():
    return {'create': 'enterprise'}