import pytest

from exdec.data_classes import FuncInfo, DecData


class CustomException(Exception):
    pass


@pytest.fixture(scope="session")
def custom_exception():
    return CustomException("exception message")


@pytest.fixture(scope="session")
def exception_classes():
    return (Exception, )


@pytest.fixture(scope="session")
def simple_func():
    def func():
        pass
    return func


@pytest.fixture()
def func_info(simple_func):
    return FuncInfo(func=simple_func, args=tuple(), kwargs=dict())


@pytest.fixture()
def dec_data(func_info, exception_classes):
    return DecData(
        exceptions=exception_classes, exclude=False, func_info=func_info
    )
