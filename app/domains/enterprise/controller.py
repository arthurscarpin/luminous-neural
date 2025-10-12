from typing import cast

from app.api.dependencies import get_enterprise_service
from app.domains.enterprise.service import EnterpriseService
from app.domains.enterprise.schema import EnterpriseCreateSchema, EnterpriseResponseSchema
from app.api.api_schemas import ResponseSchema

from fastapi import APIRouter, Depends, status


enterprise_routers = APIRouter(
    prefix='/enterprise',
    tags=['Enterprise']
)

@enterprise_routers.post(
    '/',
    response_model=ResponseSchema[EnterpriseResponseSchema],
    status_code=status.HTTP_201_CREATED,
    summary='Create a new Enterprise'
)
def create_enterprise(
    schema: EnterpriseCreateSchema,
    service: EnterpriseService = Depends(get_enterprise_service)
):
    """Create a new Enterprise record.

    Args:
        schema (EnterpriseCreateSchema): Input data for the new Enterprise.
        service (EnterpriseService, optional): Service instance provided via dependency injection.

    Returns:
        ResponseSchema[EnterpriseResponseSchema]: The created Enterprise record wrapped in a standardized response schema.
    """
    enterprise = service.create(schema)
    return cast(ResponseSchema[EnterpriseResponseSchema], ResponseSchema(data=enterprise))