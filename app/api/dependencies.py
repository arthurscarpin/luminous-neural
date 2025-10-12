from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

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
    try:
        yield session
    finally:
        session.close()

# --- Service dependency ---
def get_enterprise_service(db: Session = Depends(get_db)) -> Generator[EnterpriseService, None, None]:
    """
    Provide an EnterpriseService instance using the given DB session.

    Yields:
        EnterpriseService: Service instance.
    """
    service = EnterpriseService(db)
    try:
        yield service
    finally:
        pass
