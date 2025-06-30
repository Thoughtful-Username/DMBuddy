# src/utils/logger.py
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from src.utils.json_cache import JSONCache
import os

def setup_logger(name: str, jcache: JSONCache, **kwargs) -> logging.Logger:

    """
    Configure and return a logger instance with a rotating file handler and
    console handler which outputs to console if the logging level is 'warning'
    or above.

    Args:
        name:           Logger name. Calls to this method should use '__name__'
                        unless there is a specific reason to use something else.
        jcache:         Instance of JSONCache to load configuration from.
        **kwargs:       Optional keyword arguments to configure the logger.
                        Default values are provided in config file at:
                        data/config/config.json.  If config.json is not found or
                        otherwise invalid, the following defaults are used:
            - level:            Logging level as a string (default is 'INFO').
            - console_enabled:  Boolean to enable/disable console logging
                                (default is True).
            - console_level:    Console logging level as a string
                                (default is 'INFO).
            - console_format:   Format for console log messages
                                (default is '%(name)s - %(levelname)s: %(message)s').
            - file_enabled:     Boolean to enable/disable file logging
                                (default is True).
            - file_level:       File logging level as a string
                                (default is 'INFO').
            - file_date_fmt:    Date format for the log file name
                                (default is '%Y-%m-%d').
            - file_log_path:    Directory where log files will be stored
                                (default is 'src/logs').
            - file_maxBytes:    Maximum size of the log file before rotation
                                (default is 10MB).
            - file_backupCount: Number of backup files to keep (default is 5).
            - file_format:      Format for log messages in the file (default is 
                                '%(asctime)s - %(name)s - %(levelname)s - %(message)s').
            - log_date_fmt:     Date format for log messages in the file
                                (default is '%Y-%m-%d %H:%M:%S').
    
    Returns:
        Instance of logger
    """

    config_data = jcache.get('data/config/config.json')
    defaults = config_data.get('logger', {}).get('kwargs', {}) if config_data is not None else {}
    software = config_data.get('software', {}).get('name', 'MyApp') if config_data is not None else 'MyApp'

    # Map string level to logging level constant
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    # Default to INFO if invalid level
    level = kwargs.get('level') or defaults.get('level') or 'INFO'
    log_level = level_map.get(level.upper(), logging.INFO)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Prevent adding handlers if logger already configured
    if logger.handlers:
        return logger

    if kwargs.get('console_enabled', defaults.get('console_enabled', True)):
        # Console logging enabled
        console_level = kwargs.get('console_level',
                            defaults.get('console_level',
                                'INFO'))
        console_log_level = level_map.get(console_level.upper(), logging.INFO)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_log_level)

        # Create formatter for console
        console_format = kwargs.get('console_format',
                                    defaults.get('console_format',
                                    '%(name)s - %(levelname)s: %(message)s'))
        console_formatter = logging.Formatter(console_format)
        console_handler.setFormatter(console_formatter)

        # Add console handler to logger
        logger.addHandler(console_handler)

    if kwargs.get('file_enabled', defaults.get('file_enabled', True)):
        # File logging enabled

        print(f'{kwargs.get("file_level", defaults.get("file_level", "INFO")).upper()}')
        file_log_level = level_map.get(
                            kwargs.get('file_level',
                                defaults.get('file_level',
                                    'INFO')).upper(),
                                        logging.INFO)
        print(f'File log level: {file_log_level}')

        current_datetime = datetime.now()
        formatted_file_date = current_datetime.strftime(
                                kwargs.get('file_date_fmt',
                                    defaults.get('file_date_fmt',
                                        '%Y-%m-%d')))

        # Get maxBytes and backupCount
        max_bytes = int(kwargs.get('file_maxBytes',
                        defaults.get('file_maxBytes',
                            10485760))) # Default to 10MB
        backup_count = int(kwargs.get('file_backupCount',
                            defaults.get('file_backupCount',
                                5)))

        file_name = software + '-' + formatted_file_date + '.log'

        log_dir = kwargs.get('log_file_path',
                    defaults.get('logger', {}).get('log_file_path',
                        'src/logs'))

        # Normalize path for cross-platform compatibility
        log_dir = os.path.normpath(log_dir)

        # Create log directory if it doesn't exist
        try:
            os.makedirs(log_dir, exist_ok=True)
        except OSError as e:
            # Fallback to a temporary directory if creation fails
            log_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "logs"))
            os.makedirs(log_dir, exist_ok=True)
            logger.warning(f"Failed to create log directory {log_dir}, using fallback: {e}")

        file_formatter = logging.Formatter(kwargs.get('file_format',
                            defaults.get('file_format',
                                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')))
        file_formatter.default_time_format = kwargs.get('log_date_fmt',
                                                defaults.get('log_date_fmt',
                                                    '%Y-%m-%d %H:%M:%S'))
        
        # Create and configure file handler with rotation
        log_file = os.path.join(log_dir, f"{file_name}")
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(file_log_level)
        print(f"File log level set to: {file_log_level}")
        file_handler.setFormatter(file_formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)

    return logger

if __name__ == "__main__":
    # Example usage
    logger = setup_logger(__name__, JSONCache(), file_level="DEBUG")
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")