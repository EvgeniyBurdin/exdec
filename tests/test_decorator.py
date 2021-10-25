from exdec.decorator import catch
import asyncio


@catch
def func_1():
    return 1


def test_default_work():

    assert func_1() == 1


@catch()
async def async_func_1():
    return 1


def test_default_async_work():

    assert asyncio.run(async_func_1()) == 1


@catch()
def func_2():
    return 1 / 0


def test_default_exception_work():

    assert func_2() is None


@catch
async def async_func_2():
    return 1 / 0


def test_default_exception_async_work():

    assert asyncio.run(async_func_2()) is None


@catch(ZeroDivisionError)
def func_3():
    return 1 / 0


def test_exception_work():

    assert func_3() is None
