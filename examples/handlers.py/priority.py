from exdec.data_classes import FuncInfo
from exdec.decorator import catch as default_catch
from exdec.manager import Manager


# The standard simple handlers will be used, which are defined in
# the `exdec.handlers` module and used when creating a default `manager` in
# the `exdec.manager` module (see the logs in the terminal).

@default_catch
def func1():
    pass


func1()  # `exdec.handlers.before_handler` and `exdec.handlers.after_handler`

print()


@default_catch
def func2():
    z = 1 / 0
    print(z)


func2()  # `exdec.handlers.before_handler` and `exdec.handlers.exc_handler`

print("-"*40)


# ---------------------------------------------------------__-----------------

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
    # override only after_handler and exc_handler
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


foo()  # `exdec.handlers.before_handler` and `man_handlers.after`(!)

print()


@custom_catch
def bar():
    z = 1 / 0
    print(z)


bar()  # `exdec.handlers.before_handler` and `dec_handlers.exc`(!)

print()


@custom_catch(before_handler=ind_handlers.before)
def biz():
    pass


biz()  # `ind_handlers.before`(!) and `man_handlers.after`(!)

print()


@custom_catch(before_handler=ind_handlers.before, exc_handler=ind_handlers.exc)
def bizzzz():
    z = 1 / 0
    print(z)


bizzzz()  # `ind_handlers.before`(!) and `ind_handlers.exc`(!)
