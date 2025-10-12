from __future__ import annotations
import os
import importlib
import pkgutil
from threading import Lock
from typing import Type

from sqlalchemy import create_engine, Integer
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker, Mapped, mapped_column


# --- Declarative basis for all models ---
class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)


# --- Singleton to manage the database ---
class SQLDatabaseSettings:
    """Singleton class for managing the database connection and sessions.

    This class ensures that only one instance of the database engine and session factory
    exists throughout the application. It provides methods to create tables, get sessions,
    and import models dynamically.

    Returns:
        SQLDatabaseSettings: A singleton instance of the database settings manager.
    """
    _instance: SQLDatabaseSettings | None = None
    _lock = Lock()

    def __new__(cls, db_url: str, echo: bool = True) -> SQLDatabaseSettings:
        """Creates or returns the singleton instance of SQLDatabaseSettings.

        Ensures that only one instance of the database settings manager exists
        across the application. Thread-safe using a lock to prevent race conditions.

        Args:
            db_url (str): The database connection URL (e.g., SQLite, PostgreSQL).
            echo (bool, optional): If True, SQLAlchemy will log all SQL statements. Defaults to True.

        Returns:
            SQLDatabaseSettings: The singleton instance of the database settings manager.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_url: str, echo: bool = True) -> None:
        """Initializes the SQLDatabaseSettings singleton instance.

        Sets up the SQLAlchemy engine and session factory. This method only runs
        once for the singleton instance; subsequent calls will be ignored.

        Args:
            db_url (str): The database connection URL (e.g., SQLite, PostgreSQL).
            echo (bool, optional): If True, SQLAlchemy will log all SQL statements. Defaults to True.
        """
        if getattr(self, '_initialized', False):
            return
        self.engine = create_engine(db_url, echo=echo)
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
        self._initialized = True

    def create_tables(self, base: Type[DeclarativeBase]) -> None:
        """Creates all tables defined in the provided declarative base.

        This method iterates over all models registered with the given SQLAlchemy
        declarative base and creates the corresponding tables in the database
        if they do not already exist.

        Args:
            base (Type[DeclarativeBase]): The SQLAlchemy declarative base containing
                all model classes to be created in the database.
        """
        base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        """Creates and returns a new SQLAlchemy session.

        This session can be used to interact with the database, including
        querying, inserting, updating, and deleting records. The session
        should be closed manually after use to release resources.

        Returns:
            Session: A new SQLAlchemy session bound to the engine.
        """
        return self.SessionLocal()

    def import_models(self, package: str) -> None:
        """Dynamically imports all 'model' modules within a given package.

        This ensures that all SQLAlchemy models are registered with the
        declarative base before creating tables. It recursively scans
        the package for modules ending with 'model' and imports them.

        Args:
            package (str): The Python package path (e.g., 'app.domains')
                        where model modules should be imported from.
        """
        pkg = importlib.import_module(package)
        for _, module_name, is_pkg in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + '.'):
            if not is_pkg and module_name.endswith('model'):
                importlib.import_module(module_name)


# --- Database configuration ---
DB_DIR = '.database'
DB_FILE = 'luminous_neural.db'
os.makedirs(DB_DIR, exist_ok=True)
DB_URL = f'sqlite:///{DB_DIR}/{DB_FILE}'

# --- Create singleton and initialize DB ---
db = SQLDatabaseSettings(DB_URL)
db.import_models('app.domains')
db.create_tables(Base)
