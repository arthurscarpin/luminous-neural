from typing import List, cast

from fastapi import APIRouter, Depends, Response, status
from app.domains.enterprise.schema import EnterpriseCreateSchema, EnterpriseUpdateSchema, EnterpriseResponseSchema
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
    summary='Create a new Enterprise',
    response_description='New Enterprise created.'
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
    return cast(ResponseSchema[EnterpriseResponseSchema], ResponseSchema(data=service.create(schema)))


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
    return cast(ResponseSchema[List[EnterpriseResponseSchema]], ResponseSchema(data=service.list_all()))

@enterprise_router.get(
    '/{enterprise_id}',
    response_model=ResponseSchema[EnterpriseResponseSchema],
    summary='Query enterprise by ID',
    response_description='List the specified enterprise.'
)
def list_by_id(
    enterprise_id: int,
    service: EnterpriseService = Depends(get_enterprise_service)
):
    """
    Retrieve an enterprise by its ID.

    Args:
        id (int): Unique identifier of the enterprise.
        service (EnterpriseService, optional): Service handling enterprise operations. Defaults to Depends(get_enterprise_service).

    Returns:
        ResponseSchema[EnterpriseResponseSchema]: The enterprise data wrapped in a response schema.
    """
    return cast(ResponseSchema[EnterpriseResponseSchema], ResponseSchema(data=service.list_by_id(enterprise_id)))

@enterprise_router.put(
    '/{enterprise_id}',
    response_model=ResponseSchema[EnterpriseResponseSchema],
    summary='Update enterprise by ID',
    response_description='Update a specific enterprise.'
)
def update_by_id(
    enterprise_id: int,
    schema: EnterpriseUpdateSchema,
    service: EnterpriseService = Depends(get_enterprise_service)
):
    """
    Update an existing enterprise by its ID.

    Args:
        id (int): Unique identifier of the enterprise to update.
        schema (EnterpriseUpdateSchema): Data to update the enterprise with.
        service (EnterpriseService, optional): Service handling enterprise operations. Defaults to Depends(get_enterprise_service).

    Returns:
        ResponseSchema[EnterpriseResponseSchema]: The updated enterprise data wrapped in a response schema.
    """
    return cast(ResponseSchema[EnterpriseResponseSchema], ResponseSchema(data=service.update(enterprise_id, schema)))

@enterprise_router.delete(
    '/{enterprise_id}',
   summary='Delete enterprise by ID',
    response_description='Deletes a specific enterprise.'
)
def delete_by_id(
    enterprise_id: int,
    service: EnterpriseService = Depends(get_enterprise_service)
):
    """
    Delete an enterprise by its ID.

    Args:
        enterprise_id (int): Unique identifier of the enterprise to delete.
        service (EnterpriseService, optional): Service handling enterprise operations. Defaults to Depends(get_enterprise_service).

    Returns:
        Response: HTTP 204 No Content response indicating successful deletion.
    """
    service.delete(enterprise_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)