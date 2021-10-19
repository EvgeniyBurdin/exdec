import asyncio

from logdec.decorator import logex


class SomeException1(Exception):
    pass


class SomeException2(Exception):
    pass


def biz(*args, **kwargs):
    return "biz"


@logex(no_reraise=SomeException1, callback=biz)
async def foo():

    raise SomeException1("Exception message 1")


class SomeClass:

    @logex
    async def bar(self, i):

        raise SomeException2("Exception message 2")


if __name__ == "__main__":

    print("="*10)
    print("> foo return:", asyncio.run(foo()))

    print("="*10)
    some = SomeClass()
    print("> some.bar return:", asyncio.run(some.bar(1)))
