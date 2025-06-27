# Logger Module (`logger.py`)

## Overview

The `logger.py` module in the `DMBuddy/src/utils` directory provides a centralized logging utility for the DMBuddy application. It configures and returns Python loggers with rotating file and console output capabilities, ensuring consistent and robust logging across the application. The module is designed to support hierarchical logging, flexible configuration, and millisecond-precision timestamps for detailed debugging and auditing.

## Intended Function

The `logger.py` module serves the following purposes:

- **Create Configurable Loggers**: Provides a `setup_logger` function to create module-specific loggers with customizable names, log levels, file names, and file rotation settings.
- **Persistent Logging**: Outputs logs to rotating files in the `src/logs` directory, with filenames including the date (e.g., `DMBuddy_2025-06-27.log`) to organize logs chronologically.
- **Console Output**: Simultaneously outputs logs to the console (`sys.stdout`) for immediate feedback during development and debugging.
- **Millisecond Precision**: Formats timestamps with millisecond precision (e.g., `2025-06-27 14:25:23.123`) to support detailed timing analysis.
- **Prevent Duplicate Logging**: Ensures loggers don’t accumulate duplicate handlers, avoiding redundant log messages.
- **Future Extensibility**: Includes a placeholder for loading the log directory from a configuration file (e.g., `data/config/config.json`).

The module is intended to be used by all other modules in the DMBuddy application, typically by calling `setup_logger(__name__)` to create module-specific loggers that integrate with Python’s logging hierarchy.

## Coding Concepts Employed

- **Python Logging Module**: Utilizes Python’s built-in `logging` module for robust, thread-safe logging with hierarchical logger names (e.g., `DMBuddy.utils.logger`).
- **Rotating File Handler**: Implements `RotatingFileHandler` to manage log file size, automatically rotating files when they reach a specified size (`max_bytes`, default 1MB) and keeping a limited number of backups (`backup_count`, default 5).
- **Custom Formatter**: Defines a `MillisecondFormatter` class that extends `logging.Formatter` to format timestamps with millisecond precision, truncating microseconds to three digits.
- **Type Hints**: Uses Python type hints (e.g., `str`, `int`, `logging.Logger`) to improve code clarity and support static type checking with tools like `mypy`.
- **Error Handling**: Includes robust error handling for file operations (e.g., `OSError` when creating log files) to ensure the application fails gracefully with meaningful errors.
- **Module-Level Logger**: Instantiates a module-level logger (`log = setup_logger(__name__)`) for logging within the `logger.py` module itself, consistent with usage in other modules.
- **Directory Creation**: Uses `os.makedirs` with `exist_ok=True` to safely create the log directory, avoiding errors if it already exists.
- **Singleton Logger Pattern**: Leverages `logging.getLogger(name)` to ensure a single logger instance per name, preventing duplicate loggers across the application.
- **Handler Deduplication**: Checks `if not logger.handlers` to prevent adding duplicate handlers, ensuring consistent log output.
- **Configurable Parameters**: Supports customizable log levels (e.g., `DEBUG`, `INFO`), file names, maximum file sizes, and backup counts, with defaults for ease of use.
- **Future-Proof Design**: Includes a TODO for loading the log directory from a configuration file, facilitating future enhancements without breaking existing functionality.

## Usage

Modules should import and call `setup_logger` with `__name__` to create a module-specific logger:

```python
from src.utils.logger import setup_logger
logger = setup_logger(__name__)
logger.info("Module initialized")
```
