from typing import List, cast

from app.core.logger import logger
from app.domains.tool.service import ToolService
from app.api.dependencies import get_tool_service
from app.api.api_schemas import ResponseSchema
from app.domains.tool.schema import (
    ToolCreateSchema, 
    ToolUpdateSchema,
    ToolResponseSchema
)

from fastapi import APIRouter, Depends, Response, status

tool_router = APIRouter(
    prefix='/tool',
    tags=['Tool']
)

@tool_router.post(
    '/',
    response_model=ResponseSchema[ToolResponseSchema],
    status_code=status.HTTP_201_CREATED,
    summary='Create a new Tool',
    response_description='New Tool created.'
)
def create_tool(
    schema: ToolCreateSchema,
    service: ToolService = Depends(get_tool_service)
) -> ResponseSchema[ToolResponseSchema]:
    """
    Create a new Tool using the provided schema.

    Args:
        schema (ToolCreateSchema): Data for the new Tool.
        service (ToolService, optional): Service instance. Defaults to Depends(get_tool_service).

    Returns:
        ResponseSchema[ToolResponseSchema]: Created Tool wrapped in a response schema.
    """
    logger.info('Creating a new Tool with data: %s', schema.model_dump())
    tool = service.create(schema)
    logger.info('Tool created successfully with ID: %s', tool.id)
    return cast(ResponseSchema[ToolResponseSchema], ResponseSchema(data=tool))

@tool_router.get(
    '/',
    response_model=ResponseSchema[List[ToolResponseSchema]],
    status_code=status.HTTP_200_OK,
    summary='List all Tools',
    response_description='List of all registered Tools.'
)
def list_all_tools(
    service: ToolService = Depends(get_tool_service)
) -> ResponseSchema[List[ToolResponseSchema]]:
    """
    Retrieve a list of all registered Tools.

    Args:
        service (ToolService, optional): Service instance. Defaults to Depends(get_tool_service).

    Returns:
        ResponseSchema[List[ToolResponseSchema]]: List of Tools wrapped in a response schema.
    """
    logger.info('Retrieving all Tools from the database')
    tools = service.list_all()
    logger.info('Retrieved %d Tools', len(tools))
    return cast(ResponseSchema[List[ToolResponseSchema]], ResponseSchema(data=tools))

@tool_router.get(
    '/{tool_id}',
    response_model=ResponseSchema[ToolResponseSchema],
    summary='Query Tool by ID',
    response_description='List the specified Tool.'
)
def list_by_id(
    tool_id: int,
    service: ToolService = Depends(get_tool_service)
) -> ResponseSchema[ToolResponseSchema]:
    """
    Retrieve an Tool by its ID.

    Args:
        id (int): Unique identifier of the Tool.
        service (ToolService, optional): Service handling Tool operations. Defaults to Depends(get_tool_service).

    Returns:
        ResponseSchema[ToolResponseSchema]: The Tool data wrapped in a response schema.
    """
    logger.info('Retrieving Tool with ID: %d', tool_id)
    tool = service.list_by_id(tool_id)
    logger.info('Tool retrieved successfully: %s', tool.model_dump())
    return cast(ResponseSchema[ToolResponseSchema], ResponseSchema(data=tool))

@tool_router.put(
    '/{tool_id}',
    response_model=ResponseSchema[ToolResponseSchema],
    summary='Update Tool by ID',
    response_description='Update a specific Tool.'
)
def update_by_id(
    tool_id: int,
    schema: ToolUpdateSchema,
    service: ToolService = Depends(get_tool_service)
) -> ResponseSchema[ToolResponseSchema]:
    """
    Update an existing Tool by its ID.

    Args:
        id (int): Unique identifier of the Tool to update.
        schema (ToolUpdateSchema): Data to update the Tool with.
        service (ToolService, optional): Service handling Tool operations. Defaults to Depends(get_tool_service).

    Returns:
        ResponseSchema[ToolResponseSchema]: The updated Tool data wrapped in a response schema.
    """
    logger.info('Updating Tool with ID: %d using data: %s', tool_id, schema.model_dump())
    updated_tool = service.update(tool_id, schema)
    logger.info('Tool updated successfully: %s', updated_tool.model_dump())
    return ResponseSchema(data=ToolResponseSchema.model_validate(updated_tool))

@tool_router.delete(
    '/{tool_id}',
    summary='Logically delete an Tool by ID',
    response_description='Marks the specified Tool as inactive (logical deletion).'
)
def logical_delete_by_id(
    tool_id: int,
    service: ToolService = Depends(get_tool_service)
) -> Response:
    """
    Logically deletes an Tool by setting its status flag to False.

    This endpoint performs a soft delete, meaning the record remains in the database
    but is marked as inactive. Use this when you want to preserve historical data
    without exposing it in normal queries.

    Args:
        tool_id (int): Unique identifier of the Tool to logically delete.
        service (ToolService, optional): Service instance for Tool operations.
            Defaults to Depends(get_tool_service).

    Returns:
        Response: HTTP 204 No Content response indicating successful logical deletion.
    """
    logger.info('Initiating logical deletion for Tool with ID: %d', tool_id)
    service.logical_delete(tool_id)
    logger.info('Tool with ID %d marked as inactive successfully', tool_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)