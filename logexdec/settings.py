from logging import getLogger
from os import getenv


APP_LOGGER_NAME = getenv("DEFAULT_APP_LOGGER_NAME", "logexdec")

CLASS_LOGGER_ATTR_NAME = getenv(
    "DEFAULT_CLASS_LOGGER_ATTR_NAME", "logger"
)

FUNC_LOGGER_KWARG_NAME = getenv(
    "DEFAULT_FUNC_LOGGER_KWARG_NAME", CLASS_LOGGER_ATTR_NAME
)

# Default logger
logger = getLogger(APP_LOGGER_NAME)
