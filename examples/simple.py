import asyncio

from logexdec.decorator import logex  # as _logex


class SomeException1(Exception):
    pass


class SomeException2(Exception):
    pass


# def logex(*args, **kwargs):  # define new decorator
#     # kwargs["app_logger_name"] = "app_name"
#     return _logex(*args, **kwargs)


@logex(
    return_value=[],
    # exclude=(SomeException1, SomeException2), is_log_exclude=True
    exc_info=True,
)
async def foo():

    raise SomeException1("Exception message 1")


class MyClass:

    @logex(raise_exceptions=SomeException2, is_log_raised=True)
    async def bar(self, i):

        raise SomeException2("Exception message 2")


if __name__ == "__main__":

    print("="*10)
    print(asyncio.run(foo()))

    print("="*10)
    a = MyClass()
    print(asyncio.run(a.bar(1)))
