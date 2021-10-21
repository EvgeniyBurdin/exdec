import asyncio
import functools
import inspect
from typing import Any, Callable, Optional, Tuple, Type

from .data_classes import DecData, FuncInfo


class ExDecManagerException(Exception):
    pass


def execute_wrapper(method):
    @functools.wraps(method)
    def execute(self, handler: Callable, dec_data: DecData) -> Any:

        if dec_data.func_info.exception is not None:
            self.try_reraise(dec_data)

        if asyncio.iscoroutinefunction(method):
            async def async_func():
                return await method(self, handler, dec_data)
            return async_func()
        else:
            return method(self, handler, dec_data)

    return execute


class Manager:

    def __init__(
        self,
        default_exception_classes: Tuple[Type[Exception], ...] = (Exception, ),
        before_handler: Optional[Callable[[FuncInfo], Any]] = None,
        after_handler: Optional[Callable[[FuncInfo], Any]] = None,
        exc_handler: Optional[Callable[[FuncInfo], Any]] = None,
    ):
        self.default_exception_classes = default_exception_classes

        self.before_handler = self.default_before_handler \
            if before_handler is None else before_handler

        self.after_handler = self.default_after_handler \
            if after_handler is None else after_handler

        self.exc_handler = self.default_exc_handler \
            if exc_handler is None else exc_handler

    @staticmethod
    def check_handler(handler: Callable[[FuncInfo], Any]):

        if not callable(handler):
            msg = f"Handler '{handler}' not callable"
            raise ExDecManagerException(msg)

        is_func_info = False
        signature = inspect.signature(handler)
        for param in signature.parameters.values():
            if param.annotation is FuncInfo:
                is_func_info = True
                break

        if not is_func_info:
            msg = f"'{handler}' handler has no argument with "
            msg += f"{FuncInfo} annotation"
            raise ExDecManagerException(msg)

    def make_handlers(
        self,
        before_handler: Optional[Callable[[FuncInfo], Any]],
        after_handler: Optional[Callable[[FuncInfo], Any]],
        exc_handler: Optional[Callable[[FuncInfo], Any]],
    ) -> Tuple[Callable[[FuncInfo], Any]]:

        before_handler = self.before_handler \
            if before_handler is None else before_handler

        after_handler = self.after_handler \
            if after_handler is None else after_handler

        exc_handler = self.exc_handler \
            if exc_handler is None else exc_handler

        for handler in (before_handler, after_handler, exc_handler):
            self.check_handler(handler)

        return before_handler, after_handler, exc_handler

    def make_exceptions(self, dec_args: tuple) -> Tuple[Type[Exception], ...]:

        exceptions = dec_args
        if not dec_args or (not type(dec_args[0]) is type
           and len(dec_args) == 1 and callable(dec_args[0])):
            exceptions = self.default_exception_classes

        for exc in exceptions:
            if not type(exc) is type or not issubclass(exc, Exception):
                msg = "The positional arguments of the 'cath' decorator must "
                msg += "be subclasses of Exception. But received: "
                msg += f"{exc}, type={type(exc)}."
                raise ExDecManagerException(msg)

        return exceptions

    def default_before_handler(self, func_info: FuncInfo):

        print("log before:", func_info.func.__qualname__)

    def default_after_handler(self, func_info: FuncInfo):

        print("log after:", func_info.func.__qualname__)

    def default_exc_handler(self, func_info: FuncInfo):

        print("log exc:", type(func_info.exception), func_info.exception)

    @staticmethod
    def try_reraise(dec_data: DecData):

        func_exception = dec_data.func_info.exception
        exception_classes = dec_data.exceptions

        if dec_data.exclude:
            if isinstance(func_exception, exception_classes):
                raise
        else:
            if not isinstance(func_exception, exception_classes):
                raise

    @execute_wrapper
    def execute_handler(self, handler: Callable, dec_data: DecData):
        return handler(dec_data.func_info)

    @execute_wrapper
    async def aio_execute_handler(self, handler: Callable, dec_data: DecData):

        if asyncio.iscoroutinefunction(handler):
            return await handler(dec_data.func_info)
        else:
            return handler(dec_data.func_info)
