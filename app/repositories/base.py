from typing import Type, TypeVar, Generic, Any, List, Optional

from sqlalchemy.orm import Session
from app.core.sql_database import db, Base

T = TypeVar("T", bound=Base)

# --- Base Repository for CRUD ---
class BaseRepository(Generic[T]):
    """Generic base repository for CRUD operations.

    Args:
        Generic (TypeVar): Type of the SQLAlchemy model.
    """

    def __init__(self, model: Type[T]) -> None:
        """Initialize the repository with a model and a database session.

        Args:
            model (Type[T]): SQLAlchemy model class.
        """
        self.model: Type[T] = model
        self.session: Session = db.get_session()

    def create(self, **kwargs: Any) -> T:
        """Create a new record in the database.

        Args:
            **kwargs (Any): Fields and values for the new record.

        Returns:
            T: The newly created model instance.
        """
        obj: T = self.model(**kwargs)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def get_all(self) -> List[T]:
        """Retrieve all records of the model.

        Returns:
            List[T]: List of all model instances.
        """
        return self.session.query(self.model).all()

    def get_by_id(self, id: int) -> Optional[T]:
        """Retrieve a record by its primary key.

        Args:
            id (int): Primary key of the record.

        Returns:
            Optional[T]: Model instance if found, else None.
        """
        return self.session.query(self.model).filter(self.model.id == id).first()

    def update(self, obj: T, **kwargs: Any) -> T:
        """Update an existing record with new values.

        Args:
            obj (T): Model instance to update.
            **kwargs (Any): Fields and new values to set.

        Returns:
            T: Updated model instance.
        """
        for key, value in kwargs.items():
            setattr(obj, key, value)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, obj: T) -> None:
        """Delete a record from the database.

        Args:
            obj (T): Model instance to delete.
        """
        self.session.delete(obj)
        self.session.commit()
