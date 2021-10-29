import logging

from exdec.data_classes import FuncInfo
from exdec.decorator import catch as _catch

from logger import ColorFormatter, get_stream_logger

log_format = "%(asctime)s %(levelname)s %(name)s - %(message)s"
formatter = ColorFormatter(log_format)
logger = get_stream_logger("app_name", logging.DEBUG, formatter)


def before_handler(func_info: FuncInfo):
    logger.debug(f"Before: func_info={func_info}.")
    # Changing args
    x = func_info.args[0]
    y = func_info.args[1]
    func_info.args = (x*2, y)


def after_handler(func_info: FuncInfo):
    logger.debug(f"After: func_info={func_info}.")
    # Changing result
    func_info.result /= 2
    logger.debug(f"After change result: func_info={func_info}.")


def exc_handler(func_info: FuncInfo):
    # Recovering args
    x = func_info.args[0]
    y = func_info.args[1]
    func_info.args = (int(x/2), y)
    logger.error(f"Caught an exception! func_info={func_info}. \nRERAISE")
    raise func_info.exception


def catch(*args, **kwargs):  # define new decorator
    kwargs["before_handler"] = kwargs.get("before_handler", before_handler)
    kwargs["after_handler"] = kwargs.get("after_handler", after_handler)
    kwargs["exc_handler"] = kwargs.get("exc_handler", exc_handler)
    return _catch(*args, **kwargs)


# Catching only ZeroDivisionError
@catch(ZeroDivisionError)
def div(x: int, y: int) -> float:
    logger.info(f"div({x}, {y})")
    return x / y


print("div(9, 3) result =", div(9, 3), "\n")
div(1, 0)  # ZeroDivisionError
