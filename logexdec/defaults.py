import logging
from os import getenv


APP_LOGGER_NAME = getenv("DEFAULT_APP_LOGGER_NAME", "logexdec")

CLASS_LOGGER_ATTR_NAME = getenv(
    "DEFAULT_CLASS_LOGGER_ATTR_NAME", "logger"
)

FUNC_LOGGER_KWARG_NAME = getenv(
    "DEFAULT_FUNC_LOGGER_KWARG_NAME", CLASS_LOGGER_ATTR_NAME
)
MAIN_MESSAGE = getenv(
    "DEFAULT_MAIN_MESSAGE", "Exception occured: "
)


# Default logger
logger = logging.getLogger(APP_LOGGER_NAME)

_log_format = "%(asctime)s - [%(levelname)s] - %(name)s - "
_log_format += "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter(_log_format))
logger.addHandler(stream_handler)
