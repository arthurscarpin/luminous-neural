from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.domains.enterprise.service import EnterpriseService
from app.domains.ia_group.service import IAGroupService
from app.domains.agent.service import AgentService
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

# --- Services dependencies ---
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

def get_ia_group_service(db: Session = Depends(get_db)) -> Generator[IAGroupService, None, None]:
    """
    Provide an IAGroupService instance using the given DB session.

    Yields:
        IAGroupService: Service instance.
    """
    service = IAGroupService(db)
    logger.debug('IAGroupService instance created with session: %s', db)
    try:
        yield service
    finally:
        logger.debug('IAGroupService instance released: %s', service)

def get_agent_service(db: Session = Depends(get_db)) -> Generator[AgentService, None, None]:
    """
    Provide an AgentService instance using the given DB session.

    Yields:
        AgentService: Service instance.
    """
    service = AgentService(db)
    logger.debug('AgentService instance created with session: %s', db)
    try:
        yield service
    finally:
        logger.debug('AgentService instance released: %s', service)