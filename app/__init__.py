import logging

logger = logging.getLogger("app.logger")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(levelname)s - %(asctime)s - %(name)s - %(message)s")
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(".log")
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
