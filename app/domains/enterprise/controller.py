from typing import List, cast

from app.core.logger import logger
from app.domains.enterprise.service import EnterpriseService
from app.api.dependencies import get_enterprise_service
from app.api.api_schemas import ResponseSchema
from app.domains.enterprise.schema import (
    EnterpriseCreateSchema, 
    EnterpriseUpdateSchema, 
    EnterpriseResponseSchema
)

from fastapi import APIRouter, Depends, Response, status

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
    logger.info('Creating a new enterprise with data: %s', schema.model_dump())
    created_enterprise = service.create(schema)
    logger.info('Enterprise created successfully with ID: %s', created_enterprise.id)
    return cast(ResponseSchema[EnterpriseResponseSchema], ResponseSchema(data=created_enterprise))

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
    logger.info('Retrieving all enterprises from the database')
    enterprises = service.list_all()
    logger.info('Retrieved %d enterprises', len(enterprises))
    return cast(ResponseSchema[List[EnterpriseResponseSchema]], ResponseSchema(data=enterprises))

@enterprise_router.get(
    '/{enterprise_id}',
    response_model=ResponseSchema[EnterpriseResponseSchema],
    summary='Query enterprise by ID',
    response_description='List the specified enterprise.'
)
def list_by_id(
    enterprise_id: int,
    service: EnterpriseService = Depends(get_enterprise_service)
) -> ResponseSchema[EnterpriseResponseSchema]:
    """
    Retrieve an enterprise by its ID.

    Args:
        id (int): Unique identifier of the enterprise.
        service (EnterpriseService, optional): Service handling enterprise operations. Defaults to Depends(get_enterprise_service).

    Returns:
        ResponseSchema[EnterpriseResponseSchema]: The enterprise data wrapped in a response schema.
    """
    logger.info('Retrieving enterprise with ID: %d', enterprise_id)
    enterprise = service.list_by_id(enterprise_id)
    logger.info('Enterprise retrieved successfully: %s', enterprise.model_dump())
    return cast(ResponseSchema[EnterpriseResponseSchema], ResponseSchema(data=enterprise))

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
) -> ResponseSchema[EnterpriseResponseSchema]:
    """
    Update an existing enterprise by its ID.

    Args:
        id (int): Unique identifier of the enterprise to update.
        schema (EnterpriseUpdateSchema): Data to update the enterprise with.
        service (EnterpriseService, optional): Service handling enterprise operations. Defaults to Depends(get_enterprise_service).

    Returns:
        ResponseSchema[EnterpriseResponseSchema]: The updated enterprise data wrapped in a response schema.
    """
    logger.info('Updating enterprise with ID: %d using data: %s', enterprise_id, schema.model_dump())
    updated_enterprise = service.update(enterprise_id, schema)
    logger.info('Enterprise updated successfully: %s', updated_enterprise.model_dump())
    return ResponseSchema(data=EnterpriseResponseSchema.model_validate(updated_enterprise))

@enterprise_router.delete(
    '/{enterprise_id}',
    summary='Logically delete an enterprise by ID',
    response_description='Marks the specified enterprise as inactive (logical deletion).'
)
def logical_delete_by_id(
    enterprise_id: int,
    service: EnterpriseService = Depends(get_enterprise_service)
) -> Response:
    """
    Logically deletes an enterprise by setting its status flag to False.

    This endpoint performs a soft delete, meaning the record remains in the database
    but is marked as inactive. Use this when you want to preserve historical data
    without exposing it in normal queries.

    Args:
        enterprise_id (int): Unique identifier of the enterprise to logically delete.
        service (EnterpriseService, optional): Service instance for enterprise operations.
            Defaults to Depends(get_enterprise_service).

    Returns:
        Response: HTTP 204 No Content response indicating successful logical deletion.
    """
    logger.info('Initiating logical deletion for enterprise with ID: %d', enterprise_id)
    service.logical_delete(enterprise_id)
    logger.info('Enterprise with ID %d marked as inactive successfully', enterprise_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# --- Physical Exclusion ---
# @enterprise_router.delete(
#     '/{enterprise_id}',
#    summary='Delete enterprise by ID',
#     response_description='Deletes a specific enterprise.'
# )
# def delete_by_id(
#     enterprise_id: int,
#     service: EnterpriseService = Depends(get_enterprise_service)
# ) -> Response:
#     """
#     Delete an enterprise by its ID.

#     Args:
#         enterprise_id (int): Unique identifier of the enterprise to delete.
#         service (EnterpriseService, optional): Service handling enterprise operations. Defaults to Depends(get_enterprise_service).

#     Returns:
#         Response: HTTP 204 No Content response indicating successful deletion.
#     """
#     logger.info('Deleting enterprise with ID: %d', enterprise_id)
#     service.delete(enterprise_id)
#     logger.info('Enterprise with ID %d deleted successfully', enterprise_id)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# --- Relationship Routes ---
@enterprise_router.post(
    '/{enterprise_id}/iagroups/{ia_group_id}',
    summary='Link an IAGroup to an Enterprise',
    response_description='Successfully linked IAGroup to Enterprise.'
)
def link_ia_group_to_enterprise(
    enterprise_id: int,
    ia_group_id: int,
    service: EnterpriseService = Depends(get_enterprise_service)
) -> Response:
    """
    Link an IAGroup to an Enterprise.

    Args:
        enterprise_id (int): ID of the Enterprise.
        ia_group_id (int): ID of the IAGroup.
        service (EnterpriseService, optional): Service instance for Enterprise operations.

    Returns:
        Response: HTTP 204 No Content indicating successful linking.
    """
    logger.info('Linking IAGroup %d to Enterprise %d', ia_group_id, enterprise_id)
    service.link_ia_group(enterprise_id, ia_group_id)
    logger.info('IAGroup %d successfully linked to Enterprise %d', ia_group_id, enterprise_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@enterprise_router.delete(
    '/{enterprise_id}/iagroups/{ia_group_id}',
    summary='Unlink an IAGroup from an Enterprise',
    response_description='Successfully unlinked IAGroup from Enterprise.'
)
def unlink_ia_group_from_enterprise(
    enterprise_id: int,
    ia_group_id: int,
    service: EnterpriseService = Depends(get_enterprise_service)
) -> Response:
    """
    Remove the link between an IAGroup and an Enterprise.

    Args:
        enterprise_id (int): ID of the Enterprise.
        ia_group_id (int): ID of the IAGroup.
        service (EnterpriseService, optional): Service instance for Enterprise operations.

    Returns:
        Response: HTTP 204 No Content indicating successful unlinking.
    """
    logger.info('Unlinking IAGroup %d from Enterprise %d', ia_group_id, enterprise_id)
    service.unlink_ia_group(enterprise_id, ia_group_id)
    logger.info('IAGroup %d successfully unlinked from Enterprise %d', ia_group_id, enterprise_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@enterprise_router.get(
    '/{enterprise_id}/iagroups',
    response_model=ResponseSchema[List[int]],
    summary='List IAGroup IDs linked to an Enterprise',
    response_description='Retrieve all IAGroup IDs linked to a specific Enterprise.'
)
def list_ia_groups_of_enterprise(
    enterprise_id: int,
    service: EnterpriseService = Depends(get_enterprise_service)
) -> ResponseSchema[List[int]]:
    """
    Retrieve all IAGroup IDs linked to a given Enterprise.

    Args:
        enterprise_id (int): ID of the Enterprise.
        service (EnterpriseService, optional): Service instance for Enterprise operations.

    Returns:
        ResponseSchema[List[int]]: List of linked IAGroup IDs wrapped in a response schema.
    """
    logger.info('Listing IAGroups linked to Enterprise %d', enterprise_id)
    ia_group_ids = service.list_ia_groups(enterprise_id)
    logger.info('Enterprise %d has %d linked IAGroups', enterprise_id, len(ia_group_ids))
    return ResponseSchema(data=ia_group_ids)