# /src/utils/logger.py
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import os
from typing import Literal
import json

def setup_logger(name: str,
                 level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
                 file_name: str = "DMBuddy",
                 max_bytes: int = 10**6,
                 backup_count: int = 5,
                 log_dir: str = "src/logs") -> logging.Logger:
    """
    Configure and return a logger instance with a rotating file handler and
    console handler which outputs to console if the logging level is 'warning'
    or above.

    Args:
        name:           Logger name. Calls to this method should use '__name__'
                        unless there is a specific reason to use something else.
        level:          Logging level as defined by the logging module. Defaults
                        to 'INFO'.
        file_name:      Main part of log file name. Defaults to 'DMBuddy'.  Date
                        will be appended to this name in the format
                        'DMBuddy_YYYY-MM-DD.log'.
        max_bytes:      Max individual log file size, in bytes. Defaults to 10**6.
        backup_count:   Maximum number of log files to be stored before deleting
                        to save space.
        log_dir:        Directory for log files. Code will attempt to create
                        this directory if it does not already exist.  Code
                        checks 'data/config/config.json' for this value, but
                        defaults to 'src/logs' if not found.
    
    Returns:
        Instance of logger
    """

    # Map string level to logging level constant
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%Y-%m-%d")

    # Default to INFO if invalid level
    log_level = level_map.get(level.upper(), logging.INFO)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Prevent adding handlers if logger already configured
    if logger.handlers:
        return logger

    # Try to load log directory from config file
    try:
        with open('data/config/config.json', 'r') as config_file:
            config = json.load(config_file)
            log_dir = config.get('log_dir', log_dir)
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        pass  # Use default log_dir if config file is missing or invalid

    # Create log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )

    # Create and configure file handler with rotation
    log_file = os.path.join(log_dir, f"{file_name}_{formatted_date}.log")
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(file_formatter)

    # Create and configure console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)  # Only show warnings and above
    console_handler.setFormatter(console_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger