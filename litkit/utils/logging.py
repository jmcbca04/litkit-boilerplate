"""
Logging configuration for LitKit.

This module sets up a standardized logging system for the application.
"""

import os
import logging
import logging.handlers
from datetime import datetime
from typing import Optional


# Default log directory
DEFAULT_LOG_DIR = "logs"

# Create formatter for our logs
DEFAULT_LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"


def setup_logger(
    logger_name: str,
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    log_format: str = DEFAULT_LOG_FORMAT,
) -> logging.Logger:
    """
    Set up a logger with file and console handlers.

    Args:
        logger_name: Name of the logger
        log_file: Path to the log file (if None, only console logging is used)
        level: Logging level
        log_format: Format string for log messages

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(log_format)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler if specified
    if log_file:
        # Ensure log directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create rotating file handler (10 MB max size, 5 backup files)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_default_logger() -> logging.Logger:
    """
    Get or create the default application logger.

    Returns:
        The configured logger instance
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists(DEFAULT_LOG_DIR):
        os.makedirs(DEFAULT_LOG_DIR)

    # Generate log filename with date
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(DEFAULT_LOG_DIR, f"litkit-{today}.log")

    # Set up and return logger
    return setup_logger("litkit", log_file)


# Create default application logger
app_logger = get_default_logger()


# Convenience methods
def debug(msg: str, *args, **kwargs) -> None:
    """Log a debug message."""
    app_logger.debug(msg, *args, **kwargs)


def info(msg: str, *args, **kwargs) -> None:
    """Log an info message."""
    app_logger.info(msg, *args, **kwargs)


def warning(msg: str, *args, **kwargs) -> None:
    """Log a warning message."""
    app_logger.warning(msg, *args, **kwargs)


def error(msg: str, *args, **kwargs) -> None:
    """Log an error message."""
    app_logger.error(msg, *args, **kwargs)


def critical(msg: str, *args, **kwargs) -> None:
    """Log a critical message."""
    app_logger.critical(msg, *args, **kwargs)


def exception(msg: str, *args, **kwargs) -> None:
    """Log an exception message with traceback."""
    app_logger.exception(msg, *args, **kwargs)
