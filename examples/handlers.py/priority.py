from exdec.data_classes import FuncInfo
from exdec.decorator import catch as default_catch
from exdec.manager import Manager


# Three kinds of handlers can be defined:
#
# before_handler: Callable[[FuncInfo], None]
# after_handler: Callable[[FuncInfo], None]
# exc_handler: Callable[[FuncInfo], Any]


# By default, there are no handlers.
# If an exception occurs, then the decorated function returns `None`
@default_catch
def func():
    return 1 / 0


assert func() is None


# ----------------------------------------------------------------------------

class Handlers():

    @property
    def lbl(self) -> str:
        return f"# {self.__class__.__name__}"

    def before(self, func_info: FuncInfo) -> None:
        print(f"{self.lbl} - before: {func_info}")

    def after(self, func_info: FuncInfo) -> None:
        print(f"{self.lbl} - after: {func_info}")

    def exc(self, func_info: FuncInfo) -> float:
        print(f"{self.lbl} - exc: {func_info}")
        return 0.0


class IndividualHandlers(Handlers):
    pass


class DecoratorHandlers(Handlers):
    pass


class ManagerHandlers(Handlers):
    pass


ind_handlers = IndividualHandlers()
dec_handlers = DecoratorHandlers()
man_handlers = ManagerHandlers()


manager = Manager(
    # only after_handler and exc_handler
    after_handler=man_handlers.after,
    exc_handler=man_handlers.exc
)


def custom_catch(*args, **kwargs):
    kwargs["manager"] = kwargs.get("manager", manager)
    # override only exc_handler
    kwargs["exc_handler"] = kwargs.get("exc_handler", dec_handlers.exc)
    return default_catch(*args, **kwargs)


@custom_catch
def foo():
    pass


foo()  # `man_handlers.after`

print()


@custom_catch
def bar():
    return 1 / 0


bar()  # `dec_handlers.exc`

print()


@custom_catch(before_handler=ind_handlers.before)
def biz():
    pass


biz()  # `ind_handlers.before` and `man_handlers.after`

print()


@custom_catch(before_handler=ind_handlers.before)
def bizzzz():
    return 1 / 0


bizzzz()  # `ind_handlers.before` and `dec_handlers.exc`
