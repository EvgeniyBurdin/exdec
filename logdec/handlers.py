import asyncio
import functools
from typing import Any, Callable, Optional, Tuple, Type, Union

from .data_classes import DecData, FuncInfo


def try_reraise_and_make_callback(method):
    @functools.wraps(method)
    def exception_handler(self, dec_data: DecData, callback=None):

        self.try_reraise(dec_data.exception, dec_data.no_reraise)
        callback = self.make_callback(dec_data.callback)

        if asyncio.iscoroutinefunction(method):
            async def async_func():
                return await method(self, dec_data, callback)
            return async_func()
        else:
            return method(self, dec_data, callback)

    return exception_handler


class Handler:

    def default_callback(self, func_info: FuncInfo, exception: Exception):
        print("tmp:", func_info, exception)

    @staticmethod
    def try_reraise(
        exception: Exception,
        no_reraise: Union[Tuple[Type[Exception], ...], Type[Exception]]
    ):
        if not isinstance(exception, no_reraise):
            raise

    def make_callback(self, callback: Optional[Callable]) -> Callable:

        return self.default_callback if callback is None else callback

    @try_reraise_and_make_callback
    def exception(
        self, dec_data: DecData, callback: Callable = None
    ) -> Any:

        return callback(dec_data.func_info, dec_data.exception)

    @try_reraise_and_make_callback
    async def aio_exception(
        self, dec_data: DecData, callback: Callable = None
    ) -> Any:

        if asyncio.iscoroutinefunction(callback):
            return await callback(dec_data.func_info, dec_data.exception)
        else:
            return callback(dec_data.func_info, dec_data.exception)
