import asyncio
import functools
import inspect
from typing import Any, Callable, Optional, Tuple, Type

from .data_classes import DecData, FuncInfo


class ExDecManagerException(Exception):
    pass


def handle_wrapper(handle_exception_method: Callable[[DecData], Any]):
    @functools.wraps(handle_exception_method)
    def handle_exception(self, dec_data: DecData) -> Any:

        self.try_reraise(dec_data)
        dec_data.handler = self.select_handler(dec_data)

        if asyncio.iscoroutinefunction(handle_exception_method):
            async def async_func():
                return await handle_exception_method(self, dec_data)
            return async_func()
        else:
            return handle_exception_method(self, dec_data)

    return handle_exception


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

    @staticmethod
    def is_bound_function(dec_data: DecData) -> bool:

        func_info = dec_data.func_info
        signature = inspect.signature(func_info.func)
        bound = signature.bind(*func_info.args, **func_info.kwargs)
        arguments = bound.arguments
        owner = arguments.get("self") or arguments.get("cls")

        return bool(owner)

    def select_handler(self, dec_data: DecData) -> Callable:

        return self.default_exc_handler if dec_data.handler is None \
               else dec_data.handler

    @handle_wrapper
    def handle_exception(self, dec_data: DecData) -> Any:

        return dec_data.handler(dec_data.func_info)

    @handle_wrapper
    async def aio_handle_exception(self, dec_data: DecData) -> Any:

        if asyncio.iscoroutinefunction(dec_data.handler):
            return await dec_data.handler(dec_data.func_info)
        else:
            return dec_data.handler(dec_data.func_info)
