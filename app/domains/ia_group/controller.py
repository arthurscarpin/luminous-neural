from typing import List, cast

from app.core.logger import logger
from app.domains.ia_group.service import IAGroupService
from app.api.dependencies import get_ia_group_service
from app.api.api_schemas import ResponseSchema
from app.domains.ia_group.schema import (
    IAGroupCreateSchema, 
    IAGroupUpdateSchema,
    IAGroupResponseSchema
)

from fastapi import APIRouter, Depends, Response, status

ia_group_router = APIRouter(
    prefix='/ia_group',
    tags=['IAGroup']
)

# --- CRUD Routes ---
@ia_group_router.post(
    '/',
    response_model=ResponseSchema[IAGroupResponseSchema],
    status_code=status.HTTP_201_CREATED,
    summary='Create a new IA Group',
    response_description='New IA Group created.'
)
def create_ia_group(
    schema: IAGroupCreateSchema,
    service: IAGroupService = Depends(get_ia_group_service)
) -> ResponseSchema[IAGroupResponseSchema]:
    """
    Create a new IA Group using the provided schema.

    Args:
        schema (IAGroupCreateSchema): Data for the new IA Group.
        service (IAGroupService, optional): Service instance. Defaults to Depends(get_ia_group_service).

    Returns:
        ResponseSchema[IAGroupResponseSchema]: Created IA Group wrapped in a response schema.
    """
    logger.info('Creating a new IA Group with data: %s', schema.model_dump())
    ia_group = service.create(schema)
    logger.info('IA Group created successfully with ID: %s', ia_group.id)
    return cast(ResponseSchema[IAGroupResponseSchema], ResponseSchema(data=ia_group))

@ia_group_router.get(
    '/',
    response_model=ResponseSchema[List[IAGroupResponseSchema]],
    status_code=status.HTTP_200_OK,
    summary='List all IA Groups',
    response_description='List of all registered IA Groups.'
)
def list_all_ia_groups(
    service: IAGroupService = Depends(get_ia_group_service)
) -> ResponseSchema[List[IAGroupResponseSchema]]:
    """
    Retrieve a list of all registered IA Groups.

    Args:
        service (IAGroupService, optional): Service instance. Defaults to Depends(get_ia_group_service).

    Returns:
        ResponseSchema[List[IAGroupResponseSchema]]: List of IA Groups wrapped in a response schema.
    """
    logger.info('Retrieving all IA Groups from the database')
    ia_groups = service.list_all()
    logger.info('Retrieved %d IA Groups', len(ia_groups))
    return cast(ResponseSchema[List[IAGroupResponseSchema]], ResponseSchema(data=ia_groups))

@ia_group_router.get(
    '/{ia_group_id}',
    response_model=ResponseSchema[IAGroupResponseSchema],
    summary='Query IA Group by ID',
    response_description='List the specified IA Group.'
)
def list_by_id(
    ia_group_id: int,
    service: IAGroupService = Depends(get_ia_group_service)
) -> ResponseSchema[IAGroupResponseSchema]:
    """
    Retrieve an IA Group by its ID.

    Args:
        id (int): Unique identifier of the IA Group.
        service (IAGroupService, optional): Service handling IA Group operations. Defaults to Depends(get_ia_group_service).

    Returns:
        ResponseSchema[IAGroupResponseSchema]: The IA Group data wrapped in a response schema.
    """
    logger.info('Retrieving IA Group with ID: %d', ia_group_id)
    ia_group = service.list_by_id(ia_group_id)
    logger.info('IA Group retrieved successfully: %s', ia_group.model_dump())
    return cast(ResponseSchema[IAGroupResponseSchema], ResponseSchema(data=ia_group))

@ia_group_router.put(
    '/{ia_group_id}',
    response_model=ResponseSchema[IAGroupResponseSchema],
    summary='Update IA Group by ID',
    response_description='Update a specific IA Group.'
)
def update_by_id(
    ia_group_id: int,
    schema: IAGroupUpdateSchema,
    service: IAGroupService = Depends(get_ia_group_service)
) -> ResponseSchema[IAGroupResponseSchema]:
    """
    Update an existing IA Group by its ID.

    Args:
        id (int): Unique identifier of the IA Group to update.
        schema (IAGroupUpdateSchema): Data to update the IA Group with.
        service (IAGroupService, optional): Service handling IA Group operations. Defaults to Depends(get_ia_group_service).

    Returns:
        ResponseSchema[IAGroupResponseSchema]: The updated IA Group data wrapped in a response schema.
    """
    logger.info('Updating IA Group with ID: %d using data: %s', ia_group_id, schema.model_dump())
    updated_ia_group = service.update(ia_group_id, schema)
    logger.info('IA Group updated successfully: %s', updated_ia_group.model_dump())
    return ResponseSchema(data=IAGroupResponseSchema.model_validate(updated_ia_group))

@ia_group_router.delete(
    '/{ia_group_id}',
    summary='Logically delete an IA Group by ID',
    response_description='Marks the specified IA Group as inactive (logical deletion).'
)
def logical_delete_by_id(
    ia_group_id: int,
    service: IAGroupService = Depends(get_ia_group_service)
) -> Response:
    """
    Logically deletes an IA Group by setting its status flag to False.

    This endpoint performs a soft delete, meaning the record remains in the database
    but is marked as inactive. Use this when you want to preserve historical data
    without exposing it in normal queries.

    Args:
        ia_group_id (int): Unique identifier of the IA Group to logically delete.
        service (IAGroupService, optional): Service instance for IA Group operations.
            Defaults to Depends(get_ia_group_service).

    Returns:
        Response: HTTP 204 No Content response indicating successful logical deletion.
    """
    logger.info('Initiating logical deletion for IA Group with ID: %d', ia_group_id)
    service.logical_delete(ia_group_id)
    logger.info('IA Group with ID %d marked as inactive successfully', ia_group_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# --- Relationship Routes ---
@ia_group_router.post(
    '/{ia_group_id}/agents/{agent_id}',
    summary='Link an Agent to an IA Group',
    response_description='Successfully linked Agent to IA Group.'
)
def link_agent_to_ia_group(
    ia_group_id: int,
    agent_id: int,
    service: IAGroupService = Depends(get_ia_group_service)
) -> Response:
    """
    Link an Agent to an IA Group.

    Args:
        ia_group_id (int): ID of the IA Group.
        agent_id (int): ID of the Agent.
        service (IAGroupService, optional): Service instance for IA Group operations.

    Returns:
        Response: HTTP 204 No Content indicating successful linking.
    """
    logger.info('Linking Agent %d to IA Group %d', agent_id, ia_group_id)
    service.link_agent(ia_group_id, agent_id)
    logger.info('Agent %d successfully linked to IA Group %d', agent_id, ia_group_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ia_group_router.delete(
    '/{ia_group_id}/agents/{agent_id}',
    summary='Unlink an Agent from an IA Group',
    response_description='Successfully unlinked Agent from IA Group.'
)
def unlink_agent_from_ia_group(
    ia_group_id: int,
    agent_id: int,
    service: IAGroupService = Depends(get_ia_group_service)
) -> Response:
    """
    Remove the link between an Agent and an IA Group.

    Args:
        ia_group_id (int): ID of the IA Group.
        agent_id (int): ID of the Agent.
        service (IAGroupService, optional): Service instance for IA Group operations.

    Returns:
        Response: HTTP 204 No Content indicating successful unlinking.
    """
    logger.info('Unlinking Agent %d from IA Group %d', agent_id, ia_group_id)
    service.unlink_agent(ia_group_id, agent_id)
    logger.info('Agent %d successfully unlinked from IA Group %d', agent_id, ia_group_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ia_group_router.get(
    '/{ia_group_id}/agents',
    response_model=ResponseSchema[List[int]],
    summary='List Agents linked to an IA Group',
    response_description='Retrieve all Agent IDs linked to a specific IA Group.'
)
def list_agents_of_ia_group(
    ia_group_id: int,
    service: IAGroupService = Depends(get_ia_group_service)
) -> ResponseSchema[List[int]]:
    """
    Retrieve all Agents linked to a given IA Group.

    Args:
        ia_group_id (int): ID of the IA Group.
        service (IAGroupService, optional): Service instance for IA Group operations.

    Returns:
        ResponseSchema[List[int]]: List of linked Agent IDs wrapped in a response schema.
    """
    logger.info('Listing Agents linked to IA Group %d', ia_group_id)
    agent_ids = service.list_agents(ia_group_id)
    logger.info('IA Group %d has %d linked Agents', ia_group_id, len(agent_ids))
    return ResponseSchema(data=agent_ids)
