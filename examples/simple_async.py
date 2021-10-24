import asyncio
from typing import Optional

from exdec.data_classes import FuncInfo
from exdec.decorator import catch


# 1 --------------------------------------------------------------------------

# Catching all exceptions
@catch
async def safe_div_1(x: int, y: int) -> Optional[float]:
    return x / y


assert asyncio.run(safe_div_1(3, 3)) == 1.0
assert asyncio.run(safe_div_1(3, 0)) is None

# 2 --------------------------------------------------------------------------

HANDLER_RESULT = 0.0


def exc_handler(func_info: FuncInfo) -> float:              # <- usual handler
    msg = f"exc_handler - Caught an exception, func_info={func_info}."
    print(f"{msg} Result changed to {HANDLER_RESULT}")
    return HANDLER_RESULT


# Catching only ZeroDivisionError
@catch(ZeroDivisionError, exc_handler=exc_handler)
async def safe_div_2(x: int, y: int) -> float:              # <- async function
    return x / y


assert asyncio.run(safe_div_2(3, 0)) == HANDLER_RESULT


# 3 --------------------------------------------------------------------------

class MyException(Exception):
    pass


async def async_exc_handler(func_info: FuncInfo) -> float:  # <- async handler
    msg = f"async_exc_handler - Caught an exception, func_info={func_info}."
    print(f"{msg} Result changed to {HANDLER_RESULT}")
    return HANDLER_RESULT


# Catching all exceptions, except for MyException
@catch(MyException, exclude=True, exc_handler=async_exc_handler)
async def safe_div_3(x: int, y: int) -> float:              # <- async function
    return x / y


assert asyncio.run(safe_div_3(3, 0)) == HANDLER_RESULT


# 4 --------------------------------------------------------------------------

# For methods everything works the same
class MathFunctions:

    @catch
    async def safe_div(self, x: int, y: int) -> Optional[float]:
        return x / y

    # Catching only MyException
    @catch(MyException, exc_handler=async_exc_handler)
    async def div(self, x: int, y: int) -> float:
        return x / y


math_functions = MathFunctions()

assert asyncio.run(math_functions.safe_div(3, 0)) is None

asyncio.run(math_functions.div(3, 0))  # ZeroDivisionError
