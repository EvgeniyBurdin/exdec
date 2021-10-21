from .data_classes import FuncInfo


def before_handler(func_info: FuncInfo):

    print("log before:", func_info.func.__qualname__)


def after_handler(func_info: FuncInfo):

    print("log after:", func_info.func.__qualname__)


def exc_handler(func_info: FuncInfo):

    print("log exc:", type(func_info.exception), func_info.exception)
