import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Create a basic logger
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

# Create console handler (outputs to the terminal)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
