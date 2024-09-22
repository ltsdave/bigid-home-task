import logging

from app.consts import LOGGER_ENV_NAME
from app.utils import get_env_var

logger = logging.getLogger(get_env_var(LOGGER_ENV_NAME))
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(levelname)s - %(asctime)s - %(name)s - %(message)s")
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(".log")
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
