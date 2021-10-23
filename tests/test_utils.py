from typing import Any, Callable

import pytest

from exdec.data_classes import DecData, FuncInfo
from exdec.utils import (ExDecException, check_exception_class, check_handler,
                         try_reraise)


def test_try_reraise_success(dec_data: DecData, custom_exception: Exception):

    dec_data.func_info.exception = Exception("message")
    dec_data.exclude = False
    dec_data.exceptions = (type(custom_exception), )
    # Exception occurred not from `dec_data.exceptions` tuple, and they
    # are reraised
    with pytest.raises(Exception):
        try_reraise(dec_data)

    dec_data.func_info.exception = custom_exception
    dec_data.exclude = True
    dec_data.exceptions = (Exception, )
    # Exception occurred from the `dec_data.exceptions` tuple, but they are
    # being reraised because `exclude` is True
    with pytest.raises(type(custom_exception)):
        try_reraise(dec_data)


def test_try_reraise_fail(dec_data: DecData, custom_exception: Exception):

    dec_data.func_info.exception = custom_exception
    dec_data.exclude = False
    dec_data.exceptions = (Exception, )
    try_reraise(dec_data)

    dec_data.func_info.exception = Exception("message")
    dec_data.exclude = True
    dec_data.exceptions = (type(custom_exception), )
    try_reraise(dec_data)


def test_check_handler_success(handler: Callable[[FuncInfo], Any]):

    check_handler(handler)


def test_check_handler_fail(func: Callable):

    with pytest.raises(ExDecException):
        check_handler(1)  # Handler not callable

    with pytest.raises(ExDecException):
        # Handler has no argument with the `FuncInfo` annotation
        check_handler(func)


def test_check_exception_class_success(custom_exception: Exception):

    check_exception_class(type(custom_exception))


def test_check_exception_class_fail():

    with pytest.raises(ExDecException):
        check_exception_class(1)  # is not type

    with pytest.raises(ExDecException):
        check_exception_class(type(1))  # is not Exception subclass
