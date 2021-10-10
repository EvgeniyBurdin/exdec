import asyncio
import logging

from logexdec.decorator import logex as _logexc

logger = logging.getLogger("app_name")


class SomeException1(Exception):
    pass


class SomeException2(Exception):
    pass


def logexc(*args, **kwargs):  # define new decorator
    # kwargs["app_logger_name"] = "app_name"
    return _logexc(*args, **kwargs)


@logexc(
    return_value=[],
    # exclude=(SomeException1, SomeException2), log_exclude=True
)
async def foo():

    raise SomeException1("Exception message 1")

    return "foo result"


class MyClass:
    logger = logging.getLogger("MyClass")

    @logexc
    async def bar(self, i):
        raise SomeException1("Exception message 2")
        return "bar result"


if __name__ == "__main__":
    print("="*10)
    print(asyncio.run(foo()))

    print("="*10)
    a = MyClass()
    print(asyncio.run(a.bar(1)))
