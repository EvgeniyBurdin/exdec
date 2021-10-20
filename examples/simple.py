import asyncio

from exdec.data_classes import FuncInfo
from exdec.decorator import catch


class SomeException_1(Exception):
    pass


class SomeException_2(Exception):
    pass


async def some_handler(func_info: FuncInfo):

    return func_info


@catch(exceptions=(SomeException_1, SomeException_2), handler=some_handler)
async def foo():

    raise SomeException_1("Exception message 1")


class SomeClass:

    @classmethod
    @catch(exceptions=SomeException_1, exclude=True, handler=some_handler)
    async def bar(cls, i):

        raise SomeException_2("Exception message 2")


if __name__ == "__main__":

    print("="*10)
    print("> foo return:", asyncio.run(foo()))

    print("="*10)
    some = SomeClass()
    print("> some.bar return:", asyncio.run(some.bar(1)))
