import pytest

from exdec.data_classes import DecData
from exdec.utils import try_reraise


def test_try_reraise_successfully(dec_data: DecData, custom_exception):

    dec_data.func_info.exception = Exception("message")
    dec_data.exclude = False
    dec_data.exceptions = (type(custom_exception), )
    with pytest.raises(Exception):
        try_reraise(dec_data)

    dec_data.func_info.exception = custom_exception
    dec_data.exclude = True
    dec_data.exceptions = (Exception, )
    with pytest.raises(type(custom_exception)):
        try_reraise(dec_data)


def test_try_reraise_fail(dec_data: DecData, custom_exception):

    dec_data.func_info.exception = custom_exception
    dec_data.exclude = False
    dec_data.exceptions = (Exception, )
    try_reraise(dec_data)

    dec_data.func_info.exception = Exception("message")
    dec_data.exclude = True
    dec_data.exceptions = (type(custom_exception), )
    try_reraise(dec_data)
