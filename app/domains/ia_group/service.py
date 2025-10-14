from typing import List
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.repositories.base import BaseRepository
from app.domains.ia_group.model import IAGroup
from app.domains.ia_group.schema import (
    IAGroupCreateSchema, 
    IAGroupUpdateSchema, 
    IAGroupResponseSchema
)

from app.api.exceptions import NotFoundException

class IAGroupService:
    """
    Service class for managing IA Group entities.
    Handles creation and retrieval of IA Groups via the repository.
    """
    
    def __init__(self, session: Session):
        """
        Initialize the service with a database session.

        Args:
            session (Session): SQLAlchemy session for database operations.
        """
        self._session = session
        self._repository = BaseRepository[IAGroup, IAGroupCreateSchema](IAGroup, self._session)

    def create(self, schema: IAGroupCreateSchema) -> IAGroupResponseSchema:
        """
        Create a new IA Group using the provided schema.

        Args:
            schema (IAGroupCreateSchema): Data for the new IA Group.

        Returns:
            IAGroupResponseSchema: The created IA Group as a response schema.
        """
        logger.info('Creating a new IA Group with data: %s', schema.model_dump())
        ia_group = self._repository.create(schema)
        validated_ia_groups = IAGroupResponseSchema.model_validate(ia_group)
        logger.info('IA Group created successfully: %s', validated_ia_groups.model_dump())
        return validated_ia_groups

    def list_all(self) -> List[IAGroupResponseSchema]:
        """
        Retrieve all IA Groups from the database.

        Returns:
            List[IAGroupResponseSchema]: List of IA Groups as response schemas.
        """
        logger.info('Retrieving all IA Groups from the database')
        ia_groups = self._repository.get_all()
        validated_ia_groups = [IAGroupResponseSchema.model_validate(grp) for grp in ia_groups]
        logger.info('Retrieved %d IA Groups', len(validated_ia_groups))
        return validated_ia_groups

    def list_by_id(self, id: int) -> IAGroupResponseSchema:
        """
        Retrieve an IA Group by its ID.

        Args:
            id (int): Unique identifier of the IA Group.

        Returns:
            IAGroupResponseSchema: The IA Group data.
        """
        logger.info('Retrieving IA Group with ID: %d', id)
        ia_group = self._repository.get_by_id(id)
        
        if not ia_group:
            logger.warning('IA Group with ID %d not found', id)
            raise NotFoundException('IA Group', id)
        
        validated_ia_group = IAGroupResponseSchema.model_validate(ia_group)
        logger.info('IA Group retrieved successfully: %s', validated_ia_group.model_dump())
        return validated_ia_group
    
    def update(self, id: int, schema: IAGroupUpdateSchema) -> IAGroupResponseSchema:
        """
        Update an existing IA Group by its ID.

        Args:
            id (int): The ID of the IA Group to update.
            schema (IAGroupUpdateSchema): The data to update the IA Group with.

        Raises:
            NotFoundException: If the IA Group with the given ID does not exist.

        Returns:
            IAGroupResponseSchema: The updated IA Group data.
        """
        logger.info('Updating IA Group with ID: %d using data: %s', id, schema.model_dump())
        ia_group = self._repository.get_by_id(id)
        
        if not ia_group:
            logger.warning('IA Group with ID %d not found for update', id)
            raise NotFoundException("IA Group", id)

        updated_ia_group = self._repository.update(ia_group, schema)
        validated_ia_group = IAGroupResponseSchema.model_validate(updated_ia_group)
        logger.info('IA Group updated successfully: %s', validated_ia_group.model_dump())
        return validated_ia_group
    
    def delete(self, id: int) -> None:
        """
        Delete an IA Group by its ID.

        Args:
            id (int): Unique identifier of the IA Group to delete.

        Raises:
            NotFoundException: If no IA Group with the given ID exists.
        """
        logger.info('Deleting IA Group with ID: %d', id)
        ia_group = self._repository.get_by_id(id)
        
        if not ia_group:
            logger.warning('IA Group with ID %d not found for deletion', id)
            raise NotFoundException("IA Group", id)

        self._repository.delete(ia_group)
        logger.info('IA Group with ID %d deleted successfully', id)
  
    def logical_delete(self, id: int) -> None:
        """
        Perform a logical (soft) deletion of an IA Group by its ID.

        This method marks the IA Group as inactive (status=False) instead of physically
        removing it from the database. Useful for preserving historical data while hiding
        it from normal queries.

        Args:
            id (int): Unique identifier of the IA Group to logically delete.

        Raises:
            NotFoundException: If no IA Group with the given ID exists.
        """
        logger.info('Starting logical deletion for IA Group with ID: %d', id)
        ia_group = self._repository.get_by_id(id)
        
        if not ia_group:
            logger.warning('IA Group with ID %d not found for logical deletion', id)
            raise NotFoundException("IA Group", id)
        
        self._repository.logical_delete(ia_group)
        logger.info('Logical deletion completed: IA Group with ID %d is now inactive', id)