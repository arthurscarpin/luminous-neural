from typing import List
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.repositories.base import BaseRepository
from app.domains.tool.model import Tool
from app.domains.tool.schema import (
    ToolCreateSchema, 
    ToolUpdateSchema, 
    ToolResponseSchema
)

from app.api.exceptions import NotFoundException

class ToolService:
    """
    Service class for managing Tool entities.
    Handles creation and retrieval of Tool via the repository.
    """
    
    def __init__(self, session: Session):
        """
        Initialize the service with a database session.

        Args:
            session (Session): SQLAlchemy session for database operations.
        """
        self._session = session
        self._repository = BaseRepository[Tool, ToolCreateSchema](Tool, self._session)

    def create(self, schema: ToolCreateSchema) -> ToolResponseSchema:
        """
        Create a new Tool using the provided schema.

        Args:
            schema (ToolCreateSchema): Data for the new Tool.

        Returns:
            ToolResponseSchema: The created Tool as a response schema.
        """
        logger.info('Creating a new Tool with data: %s', schema.model_dump())
        tool = self._repository.create(schema)
        validated_tools = ToolResponseSchema.model_validate(tool)
        logger.info('Tool created successfully: %s', validated_tools.model_dump())
        return validated_tools

    def list_all(self) -> List[ToolResponseSchema]:
        """
        Retrieve all Tools from the database.

        Returns:
            List[ToolResponseSchema]: List of Tools as response schemas.
        """
        logger.info('Retrieving all Tools from the database')
        tools = self._repository.get_all()
        validated_tools = [ToolResponseSchema.model_validate(tool) for tool in tools]
        logger.info('Retrieved %d Tools', len(validated_tools))
        return validated_tools

    def list_by_id(self, id: int) -> ToolResponseSchema:
        """
        Retrieve an Tool by its ID.

        Args:
            id (int): Unique identifier of the Tool.

        Returns:
            ToolResponseSchema: The Tool data.
        """
        logger.info('Retrieving Tool with ID: %d', id)
        tool = self._repository.get_by_id(id)
        
        if not tool:
            logger.warning('Tool with ID %d not found', id)
            raise NotFoundException('Tool', id)
        
        validated_tool = ToolResponseSchema.model_validate(tool)
        logger.info('Tool retrieved successfully: %s', validated_tool.model_dump())
        return validated_tool
    
    def update(self, id: int, schema: ToolUpdateSchema) -> ToolResponseSchema:
        """
        Update an existing Tool by its ID.

        Args:
            id (int): The ID of the Tool to update.
            schema (ToolUpdateSchema): The data to update the Tool with.

        Raises:
            NotFoundException: If the Tool with the given ID does not exist.

        Returns:
            ToolResponseSchema: The updated Tool data.
        """
        logger.info('Updating Tool with ID: %d using data: %s', id, schema.model_dump())
        tool = self._repository.get_by_id(id)
        
        if not tool:
            logger.warning('Tool with ID %d not found for update', id)
            raise NotFoundException("Tool", id)

        updated_tool = self._repository.update(tool, schema)
        validated_tool = ToolResponseSchema.model_validate(updated_tool)
        logger.info('Tool updated successfully: %s', validated_tool.model_dump())
        return validated_tool
    
    def delete(self, id: int) -> None:
        """
        Delete an Tool by its ID.

        Args:
            id (int): Unique identifier of the Tool to delete.

        Raises:
            NotFoundException: If no Tool with the given ID exists.
        """
        logger.info('Deleting Tool with ID: %d', id)
        tool = self._repository.get_by_id(id)
        
        if not tool:
            logger.warning('Tool with ID %d not found for deletion', id)
            raise NotFoundException("Tool", id)

        self._repository.delete(tool)
        logger.info('Tool with ID %d deleted successfully', id)
  
    def logical_delete(self, id: int) -> None:
        """
        Perform a logical (soft) deletion of an Tool by its ID.

        This method marks the Tool as inactive (status=False) instead of physically
        removing it from the database. Useful for preserving historical data while hiding
        it from normal queries.

        Args:
            id (int): Unique identifier of the Tool to logically delete.

        Raises:
            NotFoundException: If no Tool with the given ID exists.
        """
        logger.info('Starting logical deletion for Tool with ID: %d', id)
        tool = self._repository.get_by_id(id)
        
        if not tool:
            logger.warning('Tool with ID %d not found for logical deletion', id)
            raise NotFoundException("Tool", id)
        
        self._repository.logical_delete(tool)
        logger.info('Logical deletion completed: Tool with ID %d is now inactive', id)