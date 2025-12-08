import os
import logging


def setup_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s"
    logging.basicConfig(
        level=log_level,
        format=log_format
    )
