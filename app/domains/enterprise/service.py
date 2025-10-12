from app.core.sql_database import db
from app.repositories.base import BaseRepository
from app.domains.enterprise.model import Enterprise
from app.domains.enterprise.schema import EnterpriseCreateSchema, EnterpriseResponseSchema

class EnterpriseService:
    """Service layer for the Enterprise domain, handling business logic 
    and interactions with the Enterprise repository.

    This service provides methods for creating, retrieving, updating, 
    and deleting Enterprise records in the database, ensuring proper 
    use of Pydantic schemas and database session management.
    """

    def __init__(self) -> None:
        """Initialize the EnterpriseService.

        Sets up a database session and instantiates the generic BaseRepository
        for managing Enterprise entities.
        """
        self._session = db.get_session()
        self._repository = BaseRepository[Enterprise, EnterpriseCreateSchema](Enterprise)
    
    def create(self, schema: EnterpriseCreateSchema) -> EnterpriseResponseSchema:
        """Create a new Enterprise record in the database.

        Args:
            schema (EnterpriseCreateSchema): Pydantic schema containing validated fields 
            required to create a new Enterprise.

        Returns:
            EnterpriseResponseSchema: Pydantic schema representing the newly created 
            Enterprise entity, ready to be returned in an API response.

        Notes:
            The database session is automatically closed after the operation.
        """
        try:
            enterprise = self._repository.create(schema)
            return EnterpriseResponseSchema.model_validate(enterprise)
        finally:
            self._session.close()