from typing import List, cast

from app.core.logger import logger
from app.domains.user.service import UserService
from app.api.dependencies import get_user_service
from app.api.api_schemas import ResponseSchema
from app.domains.user.schema import (
    UserCreateSchema, 
    UserUpdateSchema,
    UserResponseSchema
)

from fastapi import APIRouter, Depends, Response, status

user_router = APIRouter(
    prefix='/user',
    tags=['User']
)

# --- CRUD Router ---
@user_router.post(
    '/',
    response_model=ResponseSchema[UserResponseSchema],
    status_code=status.HTTP_201_CREATED,
    summary='Create a new User',
    response_description='New User created.'
)
def create_user(
    schema: UserCreateSchema,
    service: UserService = Depends(get_user_service)
) -> ResponseSchema[UserResponseSchema]:
    """
    Create a new User using the provided schema.

    Args:
        schema (UserCreateSchema): Data for the new User.
        service (UserService, optional): Service instance. Defaults to Depends(get_user_service).

    Returns:
        ResponseSchema[UserResponseSchema]: Created User wrapped in a response schema.
    """
    logger.info('Creating a new User with data: %s', schema.model_dump())
    user = service.create(schema)
    logger.info('User created successfully with ID: %s', user.id)
    return cast(ResponseSchema[UserResponseSchema], ResponseSchema(data=user))

@user_router.get(
    '/',
    response_model=ResponseSchema[List[UserResponseSchema]],
    status_code=status.HTTP_200_OK,
    summary='List all Users',
    response_description='List of all registered Users.'
)
def list_all_users(
    service: UserService = Depends(get_user_service)
) -> ResponseSchema[List[UserResponseSchema]]:
    """
    Retrieve a list of all registered Users.

    Args:
        service (UserService, optional): Service instance. Defaults to Depends(get_user_service).

    Returns:
        ResponseSchema[List[UserResponseSchema]]: List of Users wrapped in a response schema.
    """
    logger.info('Retrieving all Users from the database')
    users = service.list_all()
    logger.info('Retrieved %d Users', len(users))
    return cast(ResponseSchema[List[UserResponseSchema]], ResponseSchema(data=users))

@user_router.get(
    '/{user_id}',
    response_model=ResponseSchema[UserResponseSchema],
    summary='Query User by ID',
    response_description='List the specified User.'
)
def list_by_id(
    user_id: int,
    service: UserService = Depends(get_user_service)
) -> ResponseSchema[UserResponseSchema]:
    """
    Retrieve an User by its ID.

    Args:
        id (int): Unique identifier of the User.
        service (UserService, optional): Service handling User operations. Defaults to Depends(get_user_service).

    Returns:
        ResponseSchema[UserResponseSchema]: The User data wrapped in a response schema.
    """
    logger.info('Retrieving User with ID: %d', user_id)
    user = service.list_by_id(user_id)
    logger.info('User retrieved successfully: %s', user.model_dump())
    return cast(ResponseSchema[UserResponseSchema], ResponseSchema(data=user))

@user_router.put(
    '/{user_id}',
    response_model=ResponseSchema[UserResponseSchema],
    summary='Update User by ID',
    response_description='Update a specific User.'
)
def update_by_id(
    user_id: int,
    schema: UserUpdateSchema,
    service: UserService = Depends(get_user_service)
) -> ResponseSchema[UserResponseSchema]:
    """
    Update an existing User by its ID.

    Args:
        id (int): Unique identifier of the User to update.
        schema (UserUpdateSchema): Data to update the User with.
        service (UserService, optional): Service handling User operations. Defaults to Depends(get_user_service).

    Returns:
        ResponseSchema[UserResponseSchema]: The updated User data wrapped in a response schema.
    """
    logger.info('Updating User with ID: %d using data: %s', user_id, schema.model_dump())
    updated_user = service.update(user_id, schema)
    logger.info('User updated successfully: %s', updated_user.model_dump())
    return ResponseSchema(data=UserResponseSchema.model_validate(updated_user))

@user_router.delete(
    '/{user_id}',
    summary='Logically delete an User by ID',
    response_description='Marks the specified User as inactive (logical deletion).'
)
def logical_delete_by_id(
    user_id: int,
    service: UserService = Depends(get_user_service)
) -> Response:
    """
    Logically deletes an User by setting its status flag to False.

    This endpoint performs a soft delete, meaning the record remains in the database
    but is marked as inactive. Use this when you want to preserve historical data
    without exposing it in normal queries.

    Args:
        User_id (int): Unique identifier of the User to logically delete.
        service (UserService, optional): Service instance for User operations.
            Defaults to Depends(get_user_service).

    Returns:
        Response: HTTP 204 No Content response indicating successful logical deletion.
    """
    logger.info('Initiating logical deletion for User with ID: %d', user_id)
    service.logical_delete(user_id)
    logger.info('User with ID %d marked as inactive successfully', user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# --- Relationship Router ---
@user_router.post(
    '/{user_id}/enterprises/{enterprise_id}',
    summary='Link a User to an Enterprise',
    response_description='Successfully linked User to Enterprise.'
)
def link_user_to_enterprise(
    user_id: int,
    enterprise_id: int,
    service: UserService = Depends(get_user_service)
) -> Response:
    """
    Link a User to an Enterprise.

    Args:
        user_id (int): ID of the User.
        enterprise_id (int): ID of the Enterprise.
        service (UserService, optional): Service instance for User operations.

    Returns:
        Response: HTTP 204 No Content indicating successful linking.
    """
    logger.info('Linking User %d to Enterprise %d', user_id, enterprise_id)
    service.link_enterprise(user_id, enterprise_id)
    logger.info('User %d successfully linked to Enterprise %d', user_id, enterprise_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@user_router.delete(
    '/{user_id}/enterprises/{enterprise_id}',
    summary='Unlink a User from an Enterprise',
    response_description='Successfully unlinked User from Enterprise.'
)
def unlink_user_from_enterprise(
    user_id: int,
    enterprise_id: int,
    service: UserService = Depends(get_user_service)
) -> Response:
    """
    Remove the link between a User and an Enterprise.

    Args:
        user_id (int): ID of the User.
        enterprise_id (int): ID of the Enterprise.
        service (UserService, optional): Service instance for User operations.

    Returns:
        Response: HTTP 204 No Content indicating successful unlinking.
    """
    logger.info('Unlinking User %d from Enterprise %d', user_id, enterprise_id)
    service.unlink_enterprise(user_id, enterprise_id)
    logger.info('User %d successfully unlinked from Enterprise %d', user_id, enterprise_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@user_router.get(
    '/{user_id}/enterprises',
    response_model=ResponseSchema[List[int]],
    summary='List Enterprises linked to a User',
    response_description='Retrieve all Enterprise IDs linked to a specific User.'
)
def list_enterprises_of_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
) -> ResponseSchema[List[int]]:
    """
    Retrieve all Enterprises linked to a given User.

    Args:
        user_id (int): ID of the User.
        service (UserService, optional): Service instance for User operations.

    Returns:
        ResponseSchema[List[int]]: List of linked Enterprise IDs wrapped in a response schema.
    """
    logger.info('Listing Enterprises linked to User %d', user_id)
    enterprise_ids = service.list_enterprises(user_id)
    logger.info('User %d is linked to %d Enterprises', user_id, len(enterprise_ids))
    return ResponseSchema(data=enterprise_ids)