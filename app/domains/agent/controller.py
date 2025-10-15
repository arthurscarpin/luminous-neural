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

agent_router = APIRouter(
    prefix='/agent',
    tags=['Agent']
)

# --- CRUD Routes ---
@agent_router.post(
    '/',
    response_model=ResponseSchema[AgentResponseSchema],
    status_code=status.HTTP_201_CREATED,
    summary='Create a new Agent',
    response_description='New Agent created.'
)
def create_agent(
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

@agent_router.get(
    '/',
    response_model=ResponseSchema[List[AgentResponseSchema]],
    status_code=status.HTTP_200_OK,
    summary='List all Agents',
    response_description='List of all registered Agents.'
)
def list_all_agents(
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

@agent_router.get(
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

@agent_router.put(
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

@agent_router.delete(
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
        agent_id (int): Unique identifier of the Agent to logically delete.
        service (AgentService, optional): Service instance for Agent operations.
            Defaults to Depends(get_agent_service).

    Returns:
        Response: HTTP 204 No Content response indicating successful logical deletion.
    """
    logger.info('Initiating logical deletion for Agent with ID: %d', agent_id)
    service.logical_delete(agent_id)
    logger.info('Agent with ID %d marked as inactive successfully', agent_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# --- Relationship Routes ---
@agent_router.post(
    '/{agent_id}/tools/{tool_id}',
    summary='Link a Tool to an Agent',
    response_description='Associates a Tool with an Agent.'
)
def link_tool_to_agent(
    agent_id: int,
    tool_id: int,
    service: AgentService = Depends(get_agent_service)
) -> Response:
    """
    Link a Tool to an Agent using their IDs.

    Args:
        agent_id (int): ID of the Agent.
        tool_id (int): ID of the Tool.
        service (AgentService, optional): Service handling Agent operations.

    Returns:
        Response: HTTP 204 No Content response indicating successful linking.
    """
    logger.info('Linking Tool %d to Agent %d', tool_id, agent_id)
    service.link_tool(agent_id, tool_id)
    logger.info('Tool %d successfully linked to Agent %d', tool_id, agent_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@agent_router.delete(
    '/{agent_id}/tools/{tool_id}',
    summary='Unlink a Tool from an Agent',
    response_description='Removes association of a Tool from an Agent.'
)
def unlink_tool_from_agent(
    agent_id: int,
    tool_id: int,
    service: AgentService = Depends(get_agent_service)
) -> Response:
    """
    Remove the link between a Tool and an Agent.

    Args:
        agent_id (int): ID of the Agent.
        tool_id (int): ID of the Tool.
        service (AgentService, optional): Service handling Agent operations.

    Returns:
        Response: HTTP 204 No Content response indicating successful unlinking.
    """
    logger.info('Unlinking Tool %d from Agent %d', tool_id, agent_id)
    service.unlink_tool(agent_id, tool_id)
    logger.info('Tool %d successfully unlinked from Agent %d', tool_id, agent_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@agent_router.get(
    '/{agent_id}/tools',
    response_model=ResponseSchema[List[int]],
    summary='List Tools linked to an Agent',
    response_description='Retrieve all Tool IDs associated with a specific Agent.'
)
def list_tools_of_agent(
    agent_id: int,
    service: AgentService = Depends(get_agent_service)
) -> ResponseSchema[List[int]]:
    """
    Retrieve all Tool IDs linked to a given Agent.

    Args:
        agent_id (int): ID of the Agent.
        service (AgentService, optional): Service handling Agent operations.

    Returns:
        ResponseSchema[List[int]]: List of Tool IDs linked to the Agent.
    """
    logger.info('Retrieving Tools linked to Agent %d', agent_id)
    tool_ids = service.list_tools(agent_id)
    logger.info('Agent %d has %d linked Tools', agent_id, len(tool_ids))
    return ResponseSchema(data=tool_ids)