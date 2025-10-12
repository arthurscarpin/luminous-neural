from typing import List, cast

from fastapi import APIRouter, Depends, status
from app.domains.enterprise.schema import EnterpriseCreateSchema, EnterpriseResponseSchema
from app.domains.enterprise.service import EnterpriseService
from app.api.dependencies import get_enterprise_service
from app.api.api_schemas import ResponseSchema

enterprise_router = APIRouter(
    prefix='/enterprise',
    tags=['Enterprise']
)

@enterprise_router.post(
    '/',
    response_model=ResponseSchema[EnterpriseResponseSchema],
    status_code=status.HTTP_201_CREATED,
    summary='Create a new Enterprise'
)
def create_enterprise(
    schema: EnterpriseCreateSchema,
    service: EnterpriseService = Depends(get_enterprise_service)
) -> ResponseSchema[EnterpriseResponseSchema]:
    """
    Create a new enterprise using the provided schema.

    Args:
        schema (EnterpriseCreateSchema): Data for the new enterprise.
        service (EnterpriseService, optional): Service instance. Defaults to Depends(get_enterprise_service).

    Returns:
        ResponseSchema[EnterpriseResponseSchema]: Created enterprise wrapped in a response schema.
    """
    enterprise = service.create(schema)
    return cast(ResponseSchema[EnterpriseResponseSchema], ResponseSchema(data=enterprise))


@enterprise_router.get(
    '/',
    response_model=ResponseSchema[List[EnterpriseResponseSchema]],
    status_code=status.HTTP_200_OK,
    summary='List all Enterprises',
    response_description='List of all registered enterprises.'
)
def list_all_enterprises(
    service: EnterpriseService = Depends(get_enterprise_service)
) -> ResponseSchema[List[EnterpriseResponseSchema]]:
    """
    Retrieve a list of all registered enterprises.

    Args:
        service (EnterpriseService, optional): Service instance. Defaults to Depends(get_enterprise_service).

    Returns:
        ResponseSchema[List[EnterpriseResponseSchema]]: List of enterprises wrapped in a response schema.
    """
    enterprises = service.list_all()
    return cast(ResponseSchema[List[EnterpriseResponseSchema]], ResponseSchema(data=enterprises))
