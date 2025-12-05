import logging # log all information, warnings, errors, and debug messages to a file or console
import os
from datetime import datetime

'''
This module sets up logging configuration for the application.
It creates a logs directory if it doesn't exist and configures the logging
to write logs to a file named with the current date and time.

The log format includes the timestamp, line number, logger name, log level, and message.

'''

LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(log_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
