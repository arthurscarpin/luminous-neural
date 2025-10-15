from sqlalchemy import insert, delete, select
from sqlalchemy import Table
from sqlalchemy.orm import Session

from app.core.logger import logger

class ManyToManyRepository:
    """Repository for managing many-to-many association tables."""

    def __init__(self, session: Session, association_table: Table):
        """
        Initialize the repository for a specific association table.

        Args:
            session (Session): Active SQLAlchemy session.
            association_table (Table): SQLAlchemy Table representing the association.
        """
        self.session = session
        self.association_table = association_table

    def link(self, left_id: int, right_id: int, left_key: str, right_key: str) -> None:
        """
        Create a link between two entities in the association table.

        Args:
            left_id (int): ID of the first entity (e.g. agent_id).
            right_id (int): ID of the second entity (e.g. tool_id).
            left_key (str): Column name of the left entity.
            right_key (str): Column name of the right entity.
        """
        stmt = insert(self.association_table).values({left_key: left_id, right_key: right_id})
        logger.debug('Linking %s=%s with %s=%s', left_key, left_id, right_key, right_id)
        self.session.execute(stmt)
        self.session.commit()

    def unlink(self, left_id: int, right_id: int, left_key: str, right_key: str) -> None:
        """
        Remove a link between two entities in a many-to-many association table.

        Args:
            left_id (int): ID of the first entity (e.g., agent_id).
            right_id (int): ID of the second entity (e.g., tool_id).
            left_key (str): Column name of the first entity in the association table.
            right_key (str): Column name of the second entity in the association table.

        Returns:
            None
        """
        stmt = (
            delete(self.association_table)
            .where(getattr(self.association_table.c, left_key) == left_id)
            .where(getattr(self.association_table.c, right_key) == right_id)
        )
        logger.debug('Unlinking %s=%s from %s=%s', left_key, left_id, right_key, right_id)
        self.session.execute(stmt)
        self.session.commit()

    def get_links(self, left_id: int, left_key: str, right_key: str) -> list[int]:
        """
        Retrieve all linked IDs of the second entity related to a given first entity.

        Args:
            left_id (int): ID of the first entity (e.g., agent_id).
            left_key (str): Column name of the first entity in the association table.
            right_key (str): Column name of the second entity in the association table.

        Returns:
            list[int]: A list of IDs of the second entity (e.g., tool_id) linked to the given first entity.
        """
        stmt = (
            select(getattr(self.association_table.c, right_key))
            .where(getattr(self.association_table.c, left_key) == left_id)
        )
        result = self.session.execute(stmt).scalars().all()
        result_int: list[int] = [int(r) for r in result]
        logger.debug('Retrieved %d linked records for %s=%s', len(result_int), left_key, left_id)
        return result_int
