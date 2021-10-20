import asyncio
import functools
from typing import Any, Callable

from .data_classes import DecData, FuncInfo


def reraise_or_select_handler(handle_exception_method):
    @functools.wraps(handle_exception_method)
    def handle_exception(self, dec_data: DecData, handler=None):

        self.try_reraise(dec_data)
        dec_data.handler = self.select_handler(dec_data)

        if asyncio.iscoroutinefunction(handle_exception_method):
            async def async_func():
                return await handle_exception_method(self, dec_data)
            return async_func()
        else:
            return handle_exception_method(self, dec_data)

    return handle_exception


class Catcher:

    def default_handler(self, func_info: FuncInfo):
        print("--- tmp:", type(func_info.exception), func_info.exception)

    @staticmethod
    def try_reraise(dec_data: DecData):

        exception = dec_data.func_info.exception
        exceptions = dec_data.exceptions
        exclude = dec_data.exclude

        if exclude:
            if isinstance(exception, exceptions):
                raise
        else:
            if not isinstance(exception, exceptions):
                raise

    def select_handler(self, dec_data: DecData) -> Callable:

        return self.default_handler if dec_data.handler is None \
               else dec_data.handler

    @reraise_or_select_handler
    def handle_exception(self, dec_data: DecData) -> Any:

        return dec_data.handler(dec_data.func_info)

    @reraise_or_select_handler
    async def aio_handle_exception(self, dec_data: DecData) -> Any:

        if asyncio.iscoroutinefunction(dec_data.handler):
            return await dec_data.handler(dec_data.func_info)
        else:
            return dec_data.handler(dec_data.func_info)
