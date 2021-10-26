import asyncio
import functools
from typing import Any, Callable, Optional

from .data_classes import DecData, FuncInfo
from .manager import Manager

manager = Manager()


async def _async_wrapper(
    func, dec_data, manager, before_handler, after_handler, exc_handler
):
    if before_handler is not None:
        await manager.async_execute_handler(before_handler, dec_data)
    try:
        dec_data.func_info.result = await func(
            *dec_data.func_info.args, **dec_data.func_info.kwargs
        )
    except Exception as exception:
        dec_data.func_info.exception = exception
        dec_data.func_info.result = await manager.async_execute_handler(
            exc_handler, dec_data
        )
    else:
        if after_handler is not None:
            await manager.async_execute_handler(after_handler, dec_data)

    return dec_data.func_info.result


def _wrapper(
    func, dec_data, manager, before_handler, after_handler, exc_handler
):
    if before_handler is not None:
        manager.execute_handler(before_handler, dec_data)
    try:
        dec_data.func_info.result = func(
            *dec_data.func_info.args, **dec_data.func_info.kwargs
        )
    except Exception as exception:
        dec_data.func_info.exception = exception
        dec_data.func_info.result = manager.execute_handler(
            exc_handler, dec_data
        )
    else:
        if after_handler is not None:
            manager.execute_handler(after_handler, dec_data)

    return dec_data.func_info.result


def dec_args0_is_func(dec_args: tuple) -> bool:

    return dec_args and callable(dec_args[0]) and not type(dec_args[0]) is type


def catch(
    *dec_args,
    exclude: bool = False,
    before_handler: Optional[Callable[[FuncInfo], None]] = None,
    after_handler: Optional[Callable[[FuncInfo], None]] = None,
    exc_handler: Optional[Callable[[FuncInfo], Any]] = None,
    manager: Manager = manager,
    extra: Any = None,
):
    exceptions = manager.make_exceptions(dec_args)

    before_handler, after_handler, exc_handler = manager.make_handlers(
        before_handler, after_handler, exc_handler
    )

    def decor(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            func_info = FuncInfo(
                func=func, args=args, kwargs=kwargs, extra=extra
            )
            dec_data = DecData(
                exceptions=exceptions, exclude=exclude, func_info=func_info,
            )
            wrapper_args = (
                func, dec_data, manager,
                before_handler, after_handler, exc_handler
            )
            if asyncio.iscoroutinefunction(func):
                wrapper_result = _async_wrapper(*wrapper_args)
            else:
                wrapper_result = _wrapper(*wrapper_args)

            return wrapper_result

        return wrapper

    if dec_args0_is_func(dec_args):
        return decor(dec_args[0])
    else:
        return decor
