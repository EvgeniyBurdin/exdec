from typing import Tuple, Type

import pytest
from exdec.data_classes import Callable, DecData, FuncInfo, Any


class CustomException(Exception):
    pass


@pytest.fixture(scope="session")
def custom_exception() -> CustomException:
    return CustomException("Custom exception message")


@pytest.fixture(scope="session")
def exception_classes() -> Tuple[Type[Exception], ...]:
    return (Exception, )


@pytest.fixture(scope="session")
def func() -> Callable:
    def func_():
        pass
    return func_


@pytest.fixture(scope="session")
def handler() -> Callable[[FuncInfo], Any]:
    def handler_(func_info: FuncInfo):
        pass
    return handler_


@pytest.fixture()
def func_info(func):
    return FuncInfo(func=func, args=tuple(), kwargs=dict())


@pytest.fixture()
def dec_data(func_info, exception_classes):
    return DecData(
        exceptions=exception_classes, exclude=False, func_info=func_info
    )
