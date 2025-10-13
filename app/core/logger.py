import sys
from datetime import datetime
import logging
from pathlib import Path
from typing import Optional

from app.core.environment import settings

class LoggerSettings:
    """
    Singleton logger configuration class.

    Configures the Python logger based on application settings and ensures
    that only one logger instance exists across the application.

    Args:
        None
    """
    _instance: Optional['LoggerSettings'] = None
    logger: logging.Logger

    def __new__(cls):
        """
        Creates a singleton instance of LoggerConfig.

        Returns:
            LoggerConfig: The singleton instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._configure()
        return cls._instance
    
    def _configure(self) -> None:
        """
        Configures the logger with console and optional file handlers.

        Sets the log level and formatting based on settings. Ensures
        that multiple handlers are not added if already configured.
        """
        self.logger = logging.getLogger(__name__)

        # --- Avoids multiple reconfiguration ---
        if self.logger.handlers:
            return
        
        # --- Sets the log level ---
        level = getattr(logging, settings.LOG_LEVEL.upper())
        self.logger.setLevel(level)

        # --- Defines log format ---
        formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # --- Log handler configuration ---
        if not self.logger.handlers:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
            # --- Configure log file ---
            if settings.LOG_PATH:
                log_dir = Path(settings.LOG_PATH).parent if settings.LOG_PATH.endswith('.log') else Path(settings.LOG_PATH)
                log_dir.mkdir(parents=True, exist_ok=True)
                daily_filename = datetime.utcnow().strftime('%Y%m%d') + '.log'
                log_path = log_dir / daily_filename
                file_handler = logging.FileHandler(log_path, encoding='utf-8')
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """
        Returns the configured logger instance.

        Returns:
            logging.Logger: Configured logger.
        """
        return self.logger

# --- Singleton Instance ---
logger: logging.Logger = LoggerSettings().get_logger()