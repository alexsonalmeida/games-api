import logging
from logging.handlers import RotatingFileHandler
import os

if not os.path.exists("logs"):
    os.mkdir("logs")

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler("logs/app.log", maxBytes=5*1024*1024, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)