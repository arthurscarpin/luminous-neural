from typing import List
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.repositories.base import BaseRepository
from app.repositories.many_to_many import ManyToManyRepository
from app.domains.ia_group.model import IAGroup, ia_group_agent_association
from app.domains.agent.model import Agent
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
        self._many_to_many = ManyToManyRepository(self._session, ia_group_agent_association)

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

    def link_agent(self, ia_group_id: int, agent_id: int) -> None:
        """
        Link an Agent to an IA Group.

        Args:
            ia_group_id (int): The IA Group ID.
            agent_id (int): The Agent ID.

        Raises:
            NotFoundException: If IA Group or Agent does not exist.
        """
        logger.info('Linking Agent %d to IA Group %d', agent_id, ia_group_id)
        ia_group = self._repository.get_by_id(ia_group_id)
        if not ia_group:
            logger.warning('IA Group with ID %d not found for linking', ia_group_id)
            raise NotFoundException('IA Group', ia_group_id)
        agent = self._session.get(Agent, agent_id)
        if not agent:
            logger.warning('Agent with ID %d not found for linking', agent_id)
            raise NotFoundException('Agent', agent_id)
        self._many_to_many.link(ia_group_id, agent_id, left_key='ia_group_id', right_key='agent_id')
        logger.info('Agent %d successfully linked to IA Group %d', agent_id, ia_group_id)

    def unlink_agent(self, ia_group_id: int, agent_id: int) -> None:
        """
        Unlink an Agent from an IA Group.

        Args:
            ia_group_id (int): The IA Group ID.
            agent_id (int): The Agent ID.
        """
        logger.info('Unlinking Agent %d from IA Group %d', agent_id, ia_group_id)
        self._many_to_many.unlink(ia_group_id, agent_id, left_key='ia_group_id', right_key='agent_id')
        logger.info('Agent %d successfully unlinked from IA Group %d', agent_id, ia_group_id)

    def list_agents(self, ia_group_id: int) -> List[int]:
        """
        List all Agents linked to a given IA Group.

        Args:
            ia_group_id (int): The IA Group ID.

        Returns:
            List[int]: IDs of Agents linked to the IA Group.
        """
        logger.info('Retrieving linked Agents for IA Group %d', ia_group_id)
        agent_ids = self._many_to_many.get_links(ia_group_id, left_key='ia_group_id', right_key='agent_id')
        logger.info('IA Group %d has %d linked Agents', ia_group_id, len(agent_ids))
        return agent_ids