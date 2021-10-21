from logging import Logger

from .data_classes import FuncInfo
from .logger import logger as default_logger


class Handler:

    logger: Logger = default_logger

    @classmethod
    def before(cls, func_info: FuncInfo):

        cls.logger.debug(f"before: {func_info}")

    @classmethod
    def after(cls, func_info: FuncInfo):

        cls.logger.debug(f"after: {func_info}")

    @classmethod
    def exc(cls, func_info: FuncInfo):

        cls.logger.error(f"exc: {func_info}")
