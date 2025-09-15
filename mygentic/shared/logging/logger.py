"""Centralized logging using loguru."""

import sys
from pathlib import Path
from typing import Optional, Union
from loguru import logger


def get_logger(
    name: Optional[str] = None,
    level: str = "INFO",
    log_file: Optional[Union[str, Path]] = None,
    rotation: str = "10 MB",
    retention: str = "7 days",
    format_string: Optional[str] = None
):
    """Get a configured loguru logger instance.
    
    Args:
        name: Logger name (used in log messages)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs to
        rotation: When to rotate log files (size-based)
        retention: How long to keep old log files
        format_string: Custom format string for log messages
    
    Returns:
        Configured loguru logger
    """
    # Remove default handler to avoid duplicate messages
    logger.remove()
    
    # Default format with name if provided
    if format_string is None:
        if name:
            format_string = (
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<level>{level: <8}</level> | "
                f"<cyan>{name}</cyan> | "
                "<level>{message}</level>"
            )
        else:
            format_string = (
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<level>{level: <8}</level> | "
                "<level>{message}</level>"
            )
    
    # Add console handler
    logger.add(
        sys.stderr,
        format=format_string,
        level=level,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # Add file handler if specified
    if log_file:
        logger.add(
            log_file,
            format=format_string,
            level=level,
            rotation=rotation,
            retention=retention,
            backtrace=True,
            diagnose=True
        )
    
    return logger


# Create default logger instance
default_logger = get_logger()