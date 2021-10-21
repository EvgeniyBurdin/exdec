import logging


logger = logging.getLogger("exdec")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)5s - %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
