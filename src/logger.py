import os
from typing import Any
from loguru import logger
from .config import config as Config

# Configure Google Cloud Logging if in production
if os.getenv("GOOGLE_CLOUD_PROJECT"):
    import google.cloud.logging
    from google.cloud.logging.handlers import CloudLoggingHandler

    # Initialize Google Cloud Logging
    client = google.cloud.logging.Client()
    handler = CloudLoggingHandler(client, name="x-bot")
    logger.add(handler, format="{level} {message}", level=Config.LOG_LEVEL)
else:
    # Local development logging
    logger.add(
        "logs/bot.log", rotation="1 day", retention="7 days", level=Config.LOG_LEVEL
    )

# Also add console logging for all environments
logger.add(lambda msg: print(msg, end=""), level=Config.LOG_LEVEL)


def get_logger() -> Any:
    return logger
