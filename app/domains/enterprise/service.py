from typing import List
from sqlalchemy.orm import Session

from app.repositories.base import BaseRepository
from app.domains.enterprise.model import Enterprise
from app.domains.enterprise.schema import EnterpriseCreateSchema, EnterpriseResponseSchema

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
