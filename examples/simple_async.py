import asyncio
from typing import Optional

from exdec.data_classes import FuncInfo
from exdec.decorator import catch


# 1 --------------------------------------------------------------------------

# Catching all exceptions
@catch
async def safe_div_1(x: int, y: int) -> Optional[float]:          # <- async
    result = x / y
    return result


z = asyncio.run(safe_div_1(3, 3))
assert z == 1.0
z = asyncio.run(safe_div_1(3, 0))
assert z is None

# 2 --------------------------------------------------------------------------

HANDLER_RESULT = 0.0


def exc_handler(func_info: FuncInfo) -> float:                    # <- usual
    exc = func_info.exception
    print(f"Caught an exception {type(exc)}: {exc}.")
    fname = func_info.func.__name__
    args = func_info.args
    print(f"Result {fname}{args} changed to {HANDLER_RESULT}")
    return HANDLER_RESULT


# Catching only ZeroDivisionError
@catch(ZeroDivisionError, exc_handler=exc_handler)
async def safe_div_2(x: int, y: int) -> float:                    # <- async
    result = x / y
    return result


z = asyncio.run(safe_div_2(3, 0))
assert z == HANDLER_RESULT


# 3 --------------------------------------------------------------------------

class MyException(Exception):
    pass


async def async_exc_handler(func_info: FuncInfo) -> float:        # <- async
    exc = func_info.exception
    print(f"Caught an exception {type(exc)}: {exc}.")
    fname = func_info.func.__name__
    args = func_info.args
    print(f"Result {fname}{args} changed to {HANDLER_RESULT}")
    return HANDLER_RESULT


# Catching all exceptions, except for MyException
@catch(MyException, exclude=True, exc_handler=async_exc_handler)
async def safe_div_3(x: int, y: int) -> float:                    # <- async
    result = x / y
    return result


z = asyncio.run(safe_div_3(3, 0))
assert z == HANDLER_RESULT


# 4 --------------------------------------------------------------------------

class MathFunctions:

    @catch
    async def safe_div(self, x: int, y: int) -> Optional[float]:  # <- async
        result = x / y
        return result

    # Catching only MyException
    @catch(MyException, exc_handler=async_exc_handler)
    async def div(self, x: int, y: int) -> float:                 # <- async
        result = x / y
        return result


math_functions = MathFunctions()

z = asyncio.run(math_functions.safe_div(3, 0))
assert z is None

asyncio.run(math_functions.div(3, 0))  # Exception
