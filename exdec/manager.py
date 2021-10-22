import asyncio
import functools
from typing import Any, Callable, Optional, Tuple, Type

from .data_classes import DecData, FuncInfo
from .handlers import after_handler, before_handler, exc_handler
from .utils import check_exception, check_handler, try_reraise


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
        before_handler: Callable[[FuncInfo], None] = before_handler,
        after_handler: Callable[[FuncInfo], None] = after_handler,
        exc_handler: Callable[[FuncInfo], Any] = exc_handler,
        try_reraise: Callable[[DecData], None] = try_reraise,
        check_handler: Callable[
            [Callable[[FuncInfo], Any]], None
        ] = check_handler,
        check_exception: Callable[[Exception], None] = check_exception,
    ):
        self.default_exception_classes = default_exception_classes

        self.before_handler = before_handler
        self.after_handler = after_handler
        self.exc_handler = exc_handler

        self.try_reraise = try_reraise
        self.check_handler = check_handler
        self.check_exception = check_exception

    def make_handlers(
        self,
        before_handler: Optional[Callable[[FuncInfo], None]],
        after_handler: Optional[Callable[[FuncInfo], None]],
        exc_handler: Optional[Callable[[FuncInfo], Any]],
    ) -> Tuple[Callable[[FuncInfo], Any]]:

        if before_handler is None:
            before_handler = self.before_handler

        if after_handler is None:
            after_handler = self.after_handler

        if exc_handler is None:
            exc_handler = self.exc_handler

        for handler in (before_handler, after_handler, exc_handler):
            self.check_handler(handler)

        return before_handler, after_handler, exc_handler

    def make_exceptions(self, dec_args: tuple) -> Tuple[Type[Exception], ...]:

        exceptions = dec_args
        if not dec_args or (not type(dec_args[0]) is type
           and len(dec_args) == 1 and callable(dec_args[0])):
            exceptions = self.default_exception_classes

        for exception in exceptions:
            self.check_exception(exception)

        return exceptions

    @execute_wrapper
    def execute_handler(self, handler: Callable, dec_data: DecData):

        return handler(dec_data.func_info)

    @execute_wrapper
    async def aio_execute_handler(self, handler: Callable, dec_data: DecData):

        if asyncio.iscoroutinefunction(handler):
            return await handler(dec_data.func_info)
        else:
            return handler(dec_data.func_info)
