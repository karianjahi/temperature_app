import sys
import traceback
from functools import wraps

from measurementDataApp.responses.resp import unexpectedErrorResp


def handle_500(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            type_, value_, traceback_ = sys.exc_info()
            ex = traceback.format_exception(type_, value_, traceback_)
            stack_trace = ''.join(map(str, ex))
            print(stack_trace)
            return unexpectedErrorResp(error_msg=stack_trace, status=501)
    return wrapper


