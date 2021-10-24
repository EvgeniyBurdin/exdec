from exdec.data_classes import FuncInfo
from exdec.decorator import catch as _catch
from exdec.manager import Manager


# Three kinds of handlers can be defined:
#
# before_handler: Callable[[FuncInfo], None]
# after_handler: Callable[[FuncInfo], None]
# exc_handler: Callable[[FuncInfo], Any]


EXC_HANDLER_RESULT = 0.0


# You can make a handler function
def before_handler(func_info: FuncInfo) -> None:
    """ Called before the operation of the function from `func_info.func`.

    Attention!
    Can change `func_info.args` and `func_info.kwargs`, changed values will
    be used when calling `func_info.func`.
    """
    print(f"before_handler: {func_info}")


class Handlers():

    # Handler can be a method of the class
    def after(self, func_info: FuncInfo) -> None:
        """ Called after successful execution of `func_info.func`.

        Attention!
        Can change the value of `func_info.result`, and it will be used as a
        result of the `func_info.func`.
        """
        print(f"after_handler: {func_info}")

    def exc(self, func_info: FuncInfo) -> float:
        """ Called if an exception occurs during the execution of
        `func_info.func` and must be handled.

        Returns the value to be used as a result of `func_info.func`.
        """
        print(f"exc_handler: {func_info}")

        return EXC_HANDLER_RESULT


handlers = Handlers()


# ----------------------------------------------------------------------------

manager = Manager(
    before_handler=before_handler,
    after_handler=handlers.after,
    exc_handler=handlers.exc,
)


def catch(*args, **kwargs):  # define new decorator
    kwargs["manager"] = kwargs.get("manager", manager)
    return _catch(*args, **kwargs)


# ----------------------------------------------------------------------------

# Catching all exceptions
@catch  # <- new decorator
def div(x: int, y: int) -> float:
    result = x / y
    return result


z = div(4, 2)
assert z == 2.0

z = div(4, 0)
assert z == 0
