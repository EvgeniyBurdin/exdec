import asyncio
from typing import Callable

from exdec.data_classes import DecData
from exdec.decorator import _async_wrapper as async_wrapper
from exdec.decorator import _wrapper as wrapper
from exdec.manager import Manager


class FakeManager:

    def __init__(self):

        self.clear_handler_calls()

    def execute_handler(
        self, fake_handler: str, dec_data: DecData
    ):
        self.is_called[fake_handler] = True

    async def async_execute_handler(
        self, fake_handler: str, dec_data: DecData
    ):
        self.is_called[fake_handler] = True

    def clear_handler_calls(self):
        self.is_called = {
            "before_handler": False,
            "after_handler": False,
            "exc_handler": False,
        }


def func_with_exception():
    return 1 / 0


async def async_func():
    pass


async def async_func_with_exception():
    return 1 / 0


def test_wrapper(func: Callable, dec_data: DecData):

    fm = FakeManager()

    wrapper(func, dec_data, fm, None, None, "exc_handler")
    assert not fm.is_called["before_handler"]
    assert not fm.is_called["after_handler"]
    assert not fm.is_called["exc_handler"]

    fm.clear_handler_calls()

    wrapper(
        func, dec_data, fm, "before_handler", "after_handler", "exc_handler"
    )
    assert fm.is_called["before_handler"]
    assert fm.is_called["after_handler"]
    assert not fm.is_called["exc_handler"]

    fm.clear_handler_calls()

    wrapper(func_with_exception, dec_data, fm, None, None, "exc_handler")
    assert not fm.is_called["before_handler"]
    assert not fm.is_called["after_handler"]
    assert fm.is_called["exc_handler"]


def test_async_wrapper(dec_data: DecData, manager: Manager):

    fm = FakeManager()

    asyncio.run(async_wrapper(
        async_func, dec_data, fm, None, None, "exc_handler"
    ))
    assert not fm.is_called["before_handler"]
    assert not fm.is_called["after_handler"]
    assert not fm.is_called["exc_handler"]

    fm.clear_handler_calls()

    asyncio.run(async_wrapper(
        async_func, dec_data, fm,
        "before_handler", "after_handler", "exc_handler"
    ))
    assert fm.is_called["before_handler"]
    assert fm.is_called["after_handler"]
    assert not fm.is_called["exc_handler"]

    fm.clear_handler_calls()

    asyncio.run(async_wrapper(
        async_func_with_exception, dec_data, fm, None, None, "exc_handler"
    ))
    assert not fm.is_called["before_handler"]
    assert not fm.is_called["after_handler"]
    assert fm.is_called["exc_handler"]
