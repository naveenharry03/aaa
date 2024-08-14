import logging
from typing import Union, Any

class AppLogger:
    def __init__(self, log_level: Union[int, str] = logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        # Create a file handler
        file_handler = logging.FileHandler("app.log")
        file_handler.setLevel(logging.DEBUG)

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # Create a formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message: Any):
        self.logger.info(message)

    def debug(self, message: Any):
        self.logger.debug(message)

    def warning(self, message: Any):
        self.logger.warning(message)

    def error(self, message: Any, exc_info: bool = True):
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message: Any):
        self.logger.critical(message)

# Example usage
logger = AppLogger(logging.DEBUG)  # Set log level to DEBUG

logger.info("This is an info message.")
logger.debug("This is a debug message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")