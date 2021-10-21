import inspect
from typing import Any, Callable

from .data_classes import DecData, FuncInfo


class ExDecException(Exception):
    pass


def try_reraise(dec_data: DecData):

    func_exception = dec_data.func_info.exception
    exception_classes = dec_data.exceptions

    if dec_data.exclude:
        if isinstance(func_exception, exception_classes):
            raise
    else:
        if not isinstance(func_exception, exception_classes):
            raise


def check_handler(handler: Callable[[FuncInfo], Any]):

    if not callable(handler):
        msg = f"Handler '{handler}' not callable"
        raise ExDecException(msg)

    is_func_info = False
    signature = inspect.signature(handler)
    for param in signature.parameters.values():
        if param.annotation is FuncInfo:
            is_func_info = True
            break

    if not is_func_info:
        msg = f"'{handler}' handler has no argument with {FuncInfo} annotation"
        raise ExDecException(msg)


def check_exception(exception: Exception):

    if not type(exception) is type or not issubclass(exception, Exception):
        msg = "The positional arguments of the 'cath' decorator must "
        msg += "be subclasses of Exception. But received: "
        msg += f"{exception}, type={type(exception)}."
        raise ExDecException(msg)
