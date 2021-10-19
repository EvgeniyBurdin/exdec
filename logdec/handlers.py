import asyncio
import functools
from typing import Any, Callable

from .data_classes import DecData, FuncInfo


def try_reraise_set_callback(method):
    @functools.wraps(method)
    def some_exception(self, dec_data: DecData, callback=None):

        if not isinstance(dec_data.exception, dec_data.no_reraise):
            raise

        callback = dec_data.callback
        callback = self.callback if callback is None else callback

        if asyncio.iscoroutinefunction(method):
            async def async_func():
                return await method(self, dec_data, callback)
            return async_func()
        else:
            return method(self, dec_data, callback)

    return some_exception


class Handler:

    def callback(self, func_info: FuncInfo, exception: Exception):
        print(func_info, exception)

    @try_reraise_set_callback
    def exception(self, dec_data: DecData, callback: Callable = None) -> Any:

        return callback(dec_data.func_info, dec_data.exception)

    @try_reraise_set_callback
    async def aio_exception(
        self, dec_data: DecData, callback: Callable = None
    ) -> Any:

        if asyncio.iscoroutinefunction(callback):
            return await callback(dec_data.func_info, dec_data.exception)
        else:
            return callback(dec_data.func_info, dec_data.exception)
