from loguru import logger
import sys
import os
import json
from datetime import datetime
from pathlib import Path
from app.config import settings

# Create logs directory if it doesn't exist
Path("logs").mkdir(exist_ok=True)

# Remove default logger
logger.remove()

# Custom format for console
console_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

# Add console logger with color
logger.add(
    sys.stdout,
    format=console_format,
    level=settings.LOG_LEVEL,
    colorize=True,
    backtrace=True,
    diagnose=True
)

# Add file logger with rotation
logger.add(
    settings.LOG_FILE,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
    level=settings.LOG_LEVEL,
    rotation=settings.LOG_ROTATION,
    retention=f"{settings.LOG_RETENTION} days",
    compression="zip",
    backtrace=True,
    diagnose=True,
    enqueue=True
)

# FIXED: Simple JSON logger without complex formatting
logger.add(
    "logs/json.log",
    format="{message}",  # Simple format
    level=settings.LOG_LEVEL,
    rotation="100 MB",
    retention="5 days",
    filter=lambda record: record["level"].name == "INFO"  # Only log INFO level
)

def get_logger(name: str):
    """Get a logger instance with context"""
    return logger.bind(module=name)

class LoggerContext:
    """Context manager for adding context to logs"""
    def __init__(self, **kwargs):
        self.kwargs = kwargs
    
    def __enter__(self):
        self.context_logger = logger.bind(**self.kwargs)
        return self.context_logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass