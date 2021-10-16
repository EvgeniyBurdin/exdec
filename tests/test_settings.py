from logdec.settings import LogDec
from logdec.defaults import logger


# ---------------------------------------------------------------------------

class Foo:

    def __init__(self):
        self.logger = logger
        self.some_attr = "not Logger"

    def bar(self):
        pass


foo = Foo()


def bar(logger=logger):
    pass


def test_log_dec_get_owner_instance():
    assert LogDec.get_owner_instance(func=foo.bar, func_args=(foo, )) == foo
    assert LogDec.get_owner_instance(func=bar, func_args=()) is None


def test_log_dec_get_logger_from_instance():
    assert LogDec.get_logger_from_instance(foo, "logger") == logger
    assert LogDec.get_logger_from_instance(foo, "some_attr") is None
    assert LogDec.get_logger_from_instance(foo, "wrong_attr") is None
    assert LogDec.get_logger_from_instance(None, "logger") is None
