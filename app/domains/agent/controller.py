from typing import List, cast

from app.core.logger import logger
from app.domains.agent.service import AgentService
from app.api.dependencies import get_agent_service
from app.api.api_schemas import ResponseSchema
from app.domains.agent.schema import (
    AgentCreateSchema, 
    AgentUpdateSchema,
    AgentResponseSchema
)

from fastapi import APIRouter, Depends, Response, status

ia_group_router = APIRouter(
    prefix='/agent',
    tags=['Agent']
)

@ia_group_router.post(
    '/',
    response_model=ResponseSchema[AgentResponseSchema],
    status_code=status.HTTP_201_CREATED,
    summary='Create a new Agent',
    response_description='New Agent created.'
)
def create_ia_group(
    schema: AgentCreateSchema,
    service: AgentService = Depends(get_agent_service)
) -> ResponseSchema[AgentResponseSchema]:
    """
    Create a new Agent using the provided schema.

    Args:
        schema (AgentCreateSchema): Data for the new Agent.
        service (AgentService, optional): Service instance. Defaults to Depends(get_agent_service).

    Returns:
        ResponseSchema[AgentResponseSchema]: Created Agent wrapped in a response schema.
    """
    logger.info('Creating a new Agent with data: %s', schema.model_dump())
    agent = service.create(schema)
    logger.info('Agent created successfully with ID: %s', agent.id)
    return cast(ResponseSchema[AgentResponseSchema], ResponseSchema(data=agent))

@ia_group_router.get(
    '/',
    response_model=ResponseSchema[List[AgentResponseSchema]],
    status_code=status.HTTP_200_OK,
    summary='List all Agents',
    response_description='List of all registered Agents.'
)
def list_all_ia_groups(
    service: AgentService = Depends(get_agent_service)
) -> ResponseSchema[List[AgentResponseSchema]]:
    """
    Retrieve a list of all registered Agents.

    Args:
        service (AgentService, optional): Service instance. Defaults to Depends(get_agent_service).

    Returns:
        ResponseSchema[List[AgentResponseSchema]]: List of Agents wrapped in a response schema.
    """
    logger.info('Retrieving all Agents from the database')
    agents = service.list_all()
    logger.info('Retrieved %d Agents', len(agents))
    return cast(ResponseSchema[List[AgentResponseSchema]], ResponseSchema(data=agents))

@ia_group_router.get(
    '/{agent_id}',
    response_model=ResponseSchema[AgentResponseSchema],
    summary='Query Agent by ID',
    response_description='List the specified Agent.'
)
def list_by_id(
    agent_id: int,
    service: AgentService = Depends(get_agent_service)
) -> ResponseSchema[AgentResponseSchema]:
    """
    Retrieve an Agent by its ID.

    Args:
        id (int): Unique identifier of the Agent.
        service (AgentService, optional): Service handling Agent operations. Defaults to Depends(get_agent_service).

    Returns:
        ResponseSchema[AgentResponseSchema]: The Agent data wrapped in a response schema.
    """
    logger.info('Retrieving Agent with ID: %d', agent_id)
    agent = service.list_by_id(agent_id)
    logger.info('Agent retrieved successfully: %s', agent.model_dump())
    return cast(ResponseSchema[AgentResponseSchema], ResponseSchema(data=agent))

@ia_group_router.put(
    '/{agent_id}',
    response_model=ResponseSchema[AgentResponseSchema],
    summary='Update Agent by ID',
    response_description='Update a specific Agent.'
)
def update_by_id(
    agent_id: int,
    schema: AgentUpdateSchema,
    service: AgentService = Depends(get_agent_service)
) -> ResponseSchema[AgentResponseSchema]:
    """
    Update an existing Agent by its ID.

    Args:
        id (int): Unique identifier of the Agent to update.
        schema (AgentUpdateSchema): Data to update the Agent with.
        service (AgentService, optional): Service handling Agent operations. Defaults to Depends(get_agent_service).

    Returns:
        ResponseSchema[AgentResponseSchema]: The updated Agent data wrapped in a response schema.
    """
    logger.info('Updating Agent with ID: %d using data: %s', agent_id, schema.model_dump())
    updated_agent = service.update(agent_id, schema)
    logger.info('Agent updated successfully: %s', updated_agent.model_dump())
    return ResponseSchema(data=AgentResponseSchema.model_validate(updated_agent))

@ia_group_router.delete(
    '/{agent_id}',
    summary='Logically delete an Agent by ID',
    response_description='Marks the specified Agent as inactive (logical deletion).'
)
def logical_delete_by_id(
    agent_id: int,
    service: AgentService = Depends(get_agent_service)
) -> Response:
    """
    Logically deletes an Agent by setting its status flag to False.

    This endpoint performs a soft delete, meaning the record remains in the database
    but is marked as inactive. Use this when you want to preserve historical data
    without exposing it in normal queries.

    Args:
        ia_group_id (int): Unique identifier of the Agent to logically delete.
        service (AgentService, optional): Service instance for Agent operations.
            Defaults to Depends(get_agent_service).

    Returns:
        Response: HTTP 204 No Content response indicating successful logical deletion.
    """
    logger.info('Initiating logical deletion for Agent with ID: %d', agent_id)
    service.logical_delete(agent_id)
    logger.info('Agent with ID %d marked as inactive successfully', agent_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)