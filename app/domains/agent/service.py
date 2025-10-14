from typing import List
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.repositories.base import BaseRepository
from app.domains.agent.model import Agent
from app.domains.agent.schema import (
    AgentCreateSchema, 
    AgentUpdateSchema, 
    AgentResponseSchema
)

from app.api.exceptions import NotFoundException

class AgentService:
    """
    Service class for managing Agent entities.
    Handles creation and retrieval of Agent via the repository.
    """
    
    def __init__(self, session: Session):
        """
        Initialize the service with a database session.

        Args:
            session (Session): SQLAlchemy session for database operations.
        """
        self._session = session
        self._repository = BaseRepository[Agent, AgentCreateSchema](Agent, self._session)

    def create(self, schema: AgentCreateSchema) -> AgentResponseSchema:
        """
        Create a new Agent using the provided schema.

        Args:
            schema (AgentCreateSchema): Data for the new Agent.

        Returns:
            AgentResponseSchema: The created Agent as a response schema.
        """
        logger.info('Creating a new Agent with data: %s', schema.model_dump())
        agent = self._repository.create(schema)
        validated_agents = AgentResponseSchema.model_validate(agent)
        logger.info('Agent created successfully: %s', validated_agents.model_dump())
        return validated_agents

    def list_all(self) -> List[AgentResponseSchema]:
        """
        Retrieve all Agents from the database.

        Returns:
            List[AgentResponseSchema]: List of Agents as response schemas.
        """
        logger.info('Retrieving all Agents from the database')
        agents = self._repository.get_all()
        validated_agents = [AgentResponseSchema.model_validate(agt) for agt in agents]
        logger.info('Retrieved %d Agents', len(validated_agents))
        return validated_agents

    def list_by_id(self, id: int) -> AgentResponseSchema:
        """
        Retrieve an Agent by its ID.

        Args:
            id (int): Unique identifier of the Agent.

        Returns:
            AgentResponseSchema: The Agent data.
        """
        logger.info('Retrieving Agent with ID: %d', id)
        agent = self._repository.get_by_id(id)
        
        if not agent:
            logger.warning('Agent with ID %d not found', id)
            raise NotFoundException('Agent', id)
        
        validated_agent = AgentResponseSchema.model_validate(agent)
        logger.info('Agent retrieved successfully: %s', validated_agent.model_dump())
        return validated_agent
    
    def update(self, id: int, schema: AgentUpdateSchema) -> AgentResponseSchema:
        """
        Update an existing Agent by its ID.

        Args:
            id (int): The ID of the Agent to update.
            schema (AgentUpdateSchema): The data to update the Agent with.

        Raises:
            NotFoundException: If the Agent with the given ID does not exist.

        Returns:
            AgentResponseSchema: The updated Agent data.
        """
        logger.info('Updating Agent with ID: %d using data: %s', id, schema.model_dump())
        agent = self._repository.get_by_id(id)
        
        if not agent:
            logger.warning('Agent with ID %d not found for update', id)
            raise NotFoundException("Agent", id)

        updated_agent = self._repository.update(agent, schema)
        validated_agent = AgentResponseSchema.model_validate(updated_agent)
        logger.info('Agent updated successfully: %s', validated_agent.model_dump())
        return validated_agent
    
    def delete(self, id: int) -> None:
        """
        Delete an Agent by its ID.

        Args:
            id (int): Unique identifier of the Agent to delete.

        Raises:
            NotFoundException: If no Agent with the given ID exists.
        """
        logger.info('Deleting Agent with ID: %d', id)
        agent = self._repository.get_by_id(id)
        
        if not agent:
            logger.warning('Agent with ID %d not found for deletion', id)
            raise NotFoundException("Agent", id)

        self._repository.delete(agent)
        logger.info('Agent with ID %d deleted successfully', id)
  
    def logical_delete(self, id: int) -> None:
        """
        Perform a logical (soft) deletion of an Agent by its ID.

        This method marks the Agent as inactive (status=False) instead of physically
        removing it from the database. Useful for preserving historical data while hiding
        it from normal queries.

        Args:
            id (int): Unique identifier of the Agent to logically delete.

        Raises:
            NotFoundException: If no Agent with the given ID exists.
        """
        logger.info('Starting logical deletion for Agent with ID: %d', id)
        agent = self._repository.get_by_id(id)
        
        if not agent:
            logger.warning('Agent with ID %d not found for logical deletion', id)
            raise NotFoundException("Agent", id)
        
        self._repository.logical_delete(agent)
        logger.info('Logical deletion completed: Agent with ID %d is now inactive', id)