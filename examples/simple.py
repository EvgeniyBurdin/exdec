import asyncio

from exdec.data_classes import FuncInfo
from exdec.decorator import catch


class SomeException_1(Exception):
    pass


class SomeException_2(Exception):
    pass


async def some_handler(func_info: FuncInfo):

    return func_info


@catch(SomeException_1, SomeException_2, handler=some_handler)
async def foo():

    raise SomeException_1("Exception message 1")


class SomeClass:

    @classmethod
    @catch(handler=some_handler)
    async def bar(cls, i):

        raise SomeException_2("Exception message 2")


async def main():

    print("="*10)
    result = await foo()
    print("> foo return:", result)

    print("="*10)
    some = SomeClass()
    result = await some.bar(1)
    print("> some.bar return:", result)


if __name__ == "__main__":

    asyncio.run(main())
