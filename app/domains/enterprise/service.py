from typing import List
from sqlalchemy.orm import Session

from app.repositories.base import BaseRepository
from app.domains.enterprise.model import Enterprise
from app.domains.enterprise.schema import EnterpriseCreateSchema, EnterpriseUpdateSchema, EnterpriseResponseSchema, EnterpriseResponseUpdateSchema
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

    def create(self, schema: EnterpriseCreateSchema) -> EnterpriseResponseSchema:
        """
        Create a new enterprise using the provided schema.

        Args:
            schema (EnterpriseCreateSchema): Data for the new enterprise.

        Returns:
            EnterpriseResponseSchema: The created enterprise as a response schema.
        """
        enterprise = self._repository.create(schema)
        return EnterpriseResponseSchema.model_validate(enterprise)

    def list_all(self) -> List[EnterpriseResponseSchema]:
        """
        Retrieve all enterprises from the database.

        Returns:
            List[EnterpriseResponseSchema]: List of enterprises as response schemas.
        """
        enterprises = self._repository.get_all()
        return [EnterpriseResponseSchema.model_validate(ent) for ent in enterprises]

    def list_by_id(self, id: int) -> EnterpriseResponseSchema:
        """
        Retrieve an enterprise by its ID.

        Args:
            id (int): Unique identifier of the enterprise.

        Returns:
            EnterpriseResponseSchema: The enterprise data.
        """
        enterprise = self._repository.get_by_id(id)
        if not enterprise:
            raise NotFoundException('Enterprise', id)
        return EnterpriseResponseSchema.model_validate(enterprise)
    
    def update(self, id: int, schema: EnterpriseUpdateSchema) -> EnterpriseResponseUpdateSchema:
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
        enterprise = self._repository.get_by_id(id)
        
        if not enterprise:
            raise NotFoundException("Enterprise", id)

        updated_enterprise = self._repository.update(enterprise, schema)
        return EnterpriseResponseUpdateSchema.model_validate(updated_enterprise)
    
    def delete(self, id: int) -> None:
        """
        Delete an enterprise by its ID.

        Args:
            id (int): Unique identifier of the enterprise to delete.

        Raises:
            NotFoundException: If no enterprise with the given ID exists.
        """
        enterprise = self._repository.get_by_id(id)
        
        if not enterprise:
            raise NotFoundException("Enterprise", id)

        self._repository.delete(enterprise)