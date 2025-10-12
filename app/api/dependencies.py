from typing import Generator
from app.domains.enterprise.service import EnterpriseService

def get_enterprise_service() -> Generator[EnterpriseService, None, None]:
    """
    Dependency function to provide an EnterpriseService instance.

    Yields:
        EnterpriseService: Instance of the service for dependency injection.
    """
    service = EnterpriseService()
    try:
        yield service
    finally:
        pass