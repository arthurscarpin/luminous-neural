from typing import List
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.repositories.base import BaseRepository
from app.repositories.many_to_many import ManyToManyRepository
from app.domains.enterprise.model import Enterprise
from app.domains.agent.model import Agent, enterprise_agent_association
from app.domains.ia_group.model import IAGroup, enterprise_ia_group_association
from app.domains.enterprise.schema import (
    EnterpriseCreateSchema, 
    EnterpriseUpdateSchema, 
    EnterpriseResponseSchema
)

from app.api.exceptions import NotFoundException

class EnterpriseService:
    """
    Service class for managing enterprise entities.
    Handles creation and retrieval of enterprises via the repository.
    """
    
    def __init__(self, session: Session):
        """
        Initialize the service with a database session.

        Args:
            session (Session): SQLAlchemy session for database operations.
        """
        self._session = session
        self._repository = BaseRepository[Enterprise, EnterpriseCreateSchema](Enterprise, self._session)
        self._enterprise_agent = ManyToManyRepository(self._session, enterprise_agent_association)
        self._enterprise_ia_group = ManyToManyRepository(self._session, enterprise_ia_group_association)

    def create(self, schema: EnterpriseCreateSchema) -> EnterpriseResponseSchema:
        """
        Create a new enterprise using the provided schema.

        Args:
            schema (EnterpriseCreateSchema): Data for the new enterprise.

        Returns:
            EnterpriseResponseSchema: The created enterprise as a response schema.
        """
        logger.info('Creating a new enterprise with data: %s', schema.model_dump())
        enterprise = self._repository.create(schema)
        validated_enterprise = EnterpriseResponseSchema.model_validate(enterprise)
        logger.info('Enterprise created successfully: %s', validated_enterprise.model_dump())
        return validated_enterprise

    def list_all(self) -> List[EnterpriseResponseSchema]:
        """
        Retrieve all enterprises from the database.

        Returns:
            List[EnterpriseResponseSchema]: List of enterprises as response schemas.
        """
        logger.info('Retrieving all enterprises from the database')
        enterprises = self._repository.get_all()
        validated_enterprises = [EnterpriseResponseSchema.model_validate(ent) for ent in enterprises]
        logger.info('Retrieved %d enterprises', len(validated_enterprises))
        return validated_enterprises

    def list_by_id(self, id: int) -> EnterpriseResponseSchema:
        """
        Retrieve an enterprise by its ID.

        Args:
            id (int): Unique identifier of the enterprise.

        Returns:
            EnterpriseResponseSchema: The enterprise data.
        """
        logger.info('Retrieving enterprise with ID: %d', id)
        enterprise = self._repository.get_by_id(id)
        
        if not enterprise:
            logger.warning('Enterprise with ID %d not found', id)
            raise NotFoundException('Enterprise', id)
        
        validated_enterprise = EnterpriseResponseSchema.model_validate(enterprise)
        logger.info('Enterprise retrieved successfully: %s', validated_enterprise.model_dump())
        return validated_enterprise
    
    def update(self, id: int, schema: EnterpriseUpdateSchema) -> EnterpriseResponseSchema:
        """
        Update an existing enterprise by its ID.

        Args:
            id (int): The ID of the enterprise to update.
            schema (EnterpriseUpdateSchema): The data to update the enterprise with.

        Raises:
            NotFoundException: If the enterprise with the given ID does not exist.

        Returns:
            EnterpriseResponseSchema: The updated enterprise data.
        """
        logger.info('Updating enterprise with ID: %d using data: %s', id, schema.model_dump())
        enterprise = self._repository.get_by_id(id)
        
        if not enterprise:
            logger.warning('Enterprise with ID %d not found for update', id)
            raise NotFoundException("Enterprise", id)

        updated_enterprise = self._repository.update(enterprise, schema)
        validated_enterprise = EnterpriseResponseSchema.model_validate(updated_enterprise)
        logger.info('Enterprise updated successfully: %s', validated_enterprise.model_dump())
        return validated_enterprise
    
    def delete(self, id: int) -> None:
        """
        Delete an enterprise by its ID.

        Args:
            id (int): Unique identifier of the enterprise to delete.

        Raises:
            NotFoundException: If no enterprise with the given ID exists.
        """
        logger.info('Deleting enterprise with ID: %d', id)
        enterprise = self._repository.get_by_id(id)
        
        if not enterprise:
            logger.warning('Enterprise with ID %d not found for deletion', id)
            raise NotFoundException("Enterprise", id)

        self._repository.delete(enterprise)
        logger.info('Enterprise with ID %d deleted successfully', id)
  
    def logical_delete(self, id: int) -> None:
        """
        Perform a logical (soft) deletion of an enterprise by its ID.

        This method marks the enterprise as inactive (status=False) instead of physically
        removing it from the database. Useful for preserving historical data while hiding
        it from normal queries.

        Args:
            id (int): Unique identifier of the enterprise to logically delete.

        Raises:
            NotFoundException: If no enterprise with the given ID exists.
        """
        logger.info('Starting logical deletion for enterprise with ID: %d', id)
        enterprise = self._repository.get_by_id(id)
        
        if not enterprise:
            logger.warning('Enterprise with ID %d not found for logical deletion', id)
            raise NotFoundException("Enterprise", id)
        
        self._repository.logical_delete(enterprise)
        logger.info('Logical deletion completed: Enterprise with ID %d is now inactive', id)
    
    def link_ia_group(self, enterprise_id: int, ia_group_id: int) -> None:
        """
        Link an IAGroup to an Enterprise.

        Args:
            enterprise_id (int): The ID of the enterprise to which the IAGroup will be linked.
            ia_group_id (int): The ID of the IAGroup to be linked.

        Raises:
            NotFoundException: If the Enterprise with the given ID does not exist.
            NotFoundException: If the IAGroup with the given ID does not exist.
        """
        logger.info('Linking IAGroup %d to Enterprise %d', ia_group_id, enterprise_id)
        
        enterprise = self._repository.get_by_id(enterprise_id)
        if not enterprise:
            logger.warning('Enterprise with ID %d not found for linking', enterprise_id)
            raise NotFoundException('Enterprise', enterprise_id)
        
        ia_group = self._session.get(IAGroup, ia_group_id)
        if not ia_group:
            logger.warning('IAGroup with ID %d not found for linking', ia_group_id)
            raise NotFoundException('IAGroup', ia_group_id)
        
        self._enterprise_ia_group.link(
            enterprise_id,
            ia_group_id,
            left_key='enterprise_id',
            right_key='ia_group_id'
        )
        logger.info('IAGroup %d successfully linked to Enterprise %d', ia_group_id, enterprise_id)

    def unlink_ia_group(self, enterprise_id: int, ia_group_id: int) -> None:
        """
        Unlink an IAGroup from an Enterprise.

        Args:
            enterprise_id (int): The ID of the enterprise from which the IAGroup will be unlinked.
            ia_group_id (int): The ID of the IAGroup to be unlinked.
        """
        logger.info('Unlinking IAGroup %d from Enterprise %d', ia_group_id, enterprise_id)
        self._enterprise_ia_group.unlink(
            enterprise_id,
            ia_group_id,
            left_key='enterprise_id',
            right_key='ia_group_id'
        )
        logger.info('IAGroup %d successfully unlinked from Enterprise %d', ia_group_id, enterprise_id)

    def list_ia_groups(self, enterprise_id: int) -> List[int]:
        """
        List all IAGroup IDs linked to a specific Enterprise.

        Args:
            enterprise_id (int): The ID of the enterprise whose linked IAGroups will be listed.

        Returns:
            List[int]: A list of IAGroup IDs linked to the specified enterprise.
        """
        logger.info('Listing IAGroups linked to Enterprise %d', enterprise_id)
        ia_group_ids = self._enterprise_ia_group.get_links(
            enterprise_id,
            left_key='enterprise_id',
            right_key='ia_group_id'
        )
        logger.info('Enterprise %d has %d linked IAGroups', enterprise_id, len(ia_group_ids))
        return ia_group_ids