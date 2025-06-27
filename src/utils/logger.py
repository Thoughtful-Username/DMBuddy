# DMBuddy/src/utils/logger.py
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import os
from typing import Literal


def setup_logger(name: str,
                 level:Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
                 file_name:str = "DMBuddy",
                 max_bytes:int = 10**6,
                 backup_count: int = 5,
                 log_dir: str = "src/logs") -> logging.Logger:
    """
    Configure and return a logger with a rotating file handler.

    Args:
        name:           Logger name. Calls to this method should use '__name__'
                        unless there is a specific reason to use something else.
        level:          Logging level as defined by the logging module. Defaults
                        to 'INFO'.
        file_name:      Main part of log file name. Defaults to 'DMBuddy'.
        max_bytes:      Max individual log file size, in bytes. Defaults to 10**6.
        backup_count:   Maximum number of log files to be stored before deleting
                        to save space.
        log_dir:        Directory for log files. Defaults to 'src/logs'.
    
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

    # TODO: Load from data/config/config.json
    os.makedirs(log_dir, exist_ok=True)
    file_name = f"{log_dir}/{file_name}_{formatted_date}.log"

    # Default to INFO if invalid level
    log_level = level_map.get(level.upper(), logging.INFO)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Avoid duplicate handlers
    if not logger.handlers:
        # Define formatter

        formatter = MillisecondFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S.%f'
        )

        # Rotating file handler
        try:
            file_handler = RotatingFileHandler(
                file_name,
                maxBytes=max_bytes,
                backupCount=backup_count
            )
        except OSError as e:
            raise OSError(f"Failed to create log file {file_name}: {e}")

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Optional console handler for immediate feedback
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


class MillisecondFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            # Use record.msecs to format milliseconds (3 digits)
            s = datetime.fromtimestamp(record.created).strftime(datefmt)
            if '%f' in datefmt:
                s = s.replace(str(record.msecs // 1)[:3].zfill(3), '%f')
        else:
            s = datetime.fromtimestamp(record.created).isoformat()
        return s

# Module-level logger for logger.py
log = setup_logger(__name__)