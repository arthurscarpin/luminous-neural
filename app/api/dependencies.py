from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.domains.enterprise.service import EnterpriseService
from app.core.sql_database import db

# --- Database dependency ---
def get_db() -> Generator[Session, None, None]:
    """
    Provide a SQLAlchemy database session.

    Yields:
        Generator[Session, None, None]: Database session.
    """
    session = db.get_session()
    logger.debug('Database session created: %s', session)
    try:
        yield session
    finally:
        session.close()
        logger.debug('Database session closed: %s', session)

# --- Service dependency ---
def get_enterprise_service(db: Session = Depends(get_db)) -> Generator[EnterpriseService, None, None]:
    """
    Provide an EnterpriseService instance using the given DB session.

    Yields:
        EnterpriseService: Service instance.
    """
    service = EnterpriseService(db)
    logger.debug('EnterpriseService instance created with session: %s', db)
    try:
        yield service
    finally:
        logger.debug('EnterpriseService instance released: %s', service)