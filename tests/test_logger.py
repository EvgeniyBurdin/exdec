from logging import Logger

from exdec.logger import logger


def test_logger_type():

    assert isinstance(logger, Logger)
