import logging
import os

def setup_logging():
    """
    Configures centralized logging for the application.

    This function sets up a root logger with a console handler and a file handler.
    It ensures that all application-related logs are captured and formatted consistently.
    """
    # Define the log file path
    # You might want to make this configurable via environment variables or a config file
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file_path = os.path.join(log_dir, "app.log")

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Set the minimum logging level

    # Prevent adding multiple handlers if setup_logging is called multiple times
    if not logger.handlers:
        # Create a formatter for log messages
        # Includes timestamp, log level, logger name, and the actual message
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Create a console handler to output logs to stdout
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Log INFO level and above to console
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Create a file handler to output logs to a file
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG)  # Log DEBUG level and above to file
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Optional: If you want to use a specific logger for your application
    # app_logger = logging.getLogger("app")
    # app_logger.setLevel(logging.DEBUG)
    # If using app_logger, ensure handlers are added to it,
    # or ensure it propagates to the root logger.
    # By default, propagation is True.

    logging.info("Logging setup complete.")

# Example usage (can be removed or modified based on how you initialize logging)
if __name__ == "__main__":
    setup_logging()
    logging.debug("This is a debug message.")
    logging.info("This is an info message.")
    logging.warning("This is a warning message.")
    logging.error("This is an error message.")
    logging.critical("This is a critical message.")
