from typing import Any, Callable, Tuple, Type

import pytest
from exdec.data_classes import DecData, FuncInfo
from exdec.manager import Manager


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
def func_info(func: Callable) -> FuncInfo:
    return FuncInfo(func=func, args=tuple(), kwargs=dict())


@pytest.fixture()
def dec_data(
    func_info: FuncInfo, exception_classes: Tuple[Type[Exception], ...]
) -> DecData:
    return DecData(
        exceptions=exception_classes, exclude=False, func_info=func_info
    )


@pytest.fixture()
def manager() -> Manager:
    return Manager()
