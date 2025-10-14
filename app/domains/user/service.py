from typing import List
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.repositories.base import BaseRepository
from app.domains.user.model import User
from app.domains.user.schema import (
    UserCreateSchema, 
    UserUpdateSchema, 
    UserResponseSchema
)
from app.utils.security import hash_password

from app.api.exceptions import NotFoundException

class UserService:
    """
    Service class for managing User entities.
    Handles creation and retrieval of User via the repository.
    """
    
    def __init__(self, session: Session):
        """
        Initialize the service with a database session.

        Args:
            session (Session): SQLAlchemy session for database operations.
        """
        self._session = session
        self._repository = BaseRepository[User, UserCreateSchema](User, self._session)

    def create(self, schema: UserCreateSchema) -> UserResponseSchema:
        """
        Create a new User using the provided schema.

        Args:
            schema (UserCreateSchema): Data for the new User.

        Returns:
            UserResponseSchema: The created User as a response schema.
        """
        logger.info('Creating a new User with data: %s', schema.model_dump())
        schema.password = hash_password(schema.password)
        user = self._repository.create(schema)
        validated_users = UserResponseSchema.model_validate(user)
        logger.info('User created successfully: %s', validated_users.model_dump())
        return validated_users

    def list_all(self) -> List[UserResponseSchema]:
        """
        Retrieve all Users from the database.

        Returns:
            List[UserResponseSchema]: List of Users as response schemas.
        """
        logger.info('Retrieving all Users from the database')
        users = self._repository.get_all()
        validated_users = [UserResponseSchema.model_validate(usr) for usr in users]
        logger.info('Retrieved %d Users', len(validated_users))
        return validated_users

    def list_by_id(self, id: int) -> UserResponseSchema:
        """
        Retrieve an User by its ID.

        Args:
            id (int): Unique identifier of the User.

        Returns:
            UserResponseSchema: The User data.
        """
        logger.info('Retrieving User with ID: %d', id)
        user = self._repository.get_by_id(id)
        
        if not user:
            logger.warning('User with ID %d not found', id)
            raise NotFoundException('User', id)
        
        validated_user = UserResponseSchema.model_validate(user)
        logger.info('User retrieved successfully: %s', validated_user.model_dump())
        return validated_user
    
    def update(self, id: int, schema: UserUpdateSchema) -> UserResponseSchema:
        """
        Update an existing User by its ID.

        Args:
            id (int): The ID of the User to update.
            schema (UserUpdateSchema): The data to update the User with.

        Raises:
            NotFoundException: If the User with the given ID does not exist.

        Returns:
            UserResponseSchema: The updated User data.
        """
        logger.info('Updating User with ID: %d using data: %s', id, schema.model_dump())
        user = self._repository.get_by_id(id)
        
        if not user:
            logger.warning('User with ID %d not found for update', id)
            raise NotFoundException("User", id)
        
        if schema.password:
            schema.password = hash_password(schema.password)

        updated_user = self._repository.update(user, schema)
        validated_user = UserResponseSchema.model_validate(updated_user)
        logger.info('User updated successfully: %s', validated_user.model_dump())
        return validated_user
    
    def delete(self, id: int) -> None:
        """
        Delete an User by its ID.

        Args:
            id (int): Unique identifier of the User to delete.

        Raises:
            NotFoundException: If no User with the given ID exists.
        """
        logger.info('Deleting User with ID: %d', id)
        user = self._repository.get_by_id(id)
        
        if not user:
            logger.warning('User with ID %d not found for deletion', id)
            raise NotFoundException("User", id)

        self._repository.delete(user)
        logger.info('User with ID %d deleted successfully', id)
  
    def logical_delete(self, id: int) -> None:
        """
        Perform a logical (soft) deletion of an User by its ID.

        This method marks the User as inactive (status=False) instead of physically
        removing it from the database. Useful for preserving historical data while hiding
        it from normal queries.

        Args:
            id (int): Unique identifier of the User to logically delete.

        Raises:
            NotFoundException: If no User with the given ID exists.
        """
        logger.info('Starting logical deletion for User with ID: %d', id)
        user = self._repository.get_by_id(id)
        
        if not user:
            logger.warning('User with ID %d not found for logical deletion', id)
            raise NotFoundException("User", id)
        
        self._repository.logical_delete(user)
        logger.info('Logical deletion completed: User with ID %d is now inactive', id)