from functools import wraps
from typing import Callable, TypeVar

T = TypeVar('T')
Test = Callable[[T], bool]


def user_passes_test(test: Test, exception: Exception = None):
    def decorator(func):
        @wraps(func)
        def wrapper(_root, _info, *args, **kwargs):
            if test(_info.context.user):
                return func(_root, _info, *args, **kwargs)

            if exception is not None:
                raise exception
        return wrapper

    return decorator


def login_required():
    return user_passes_test(lambda user: user.is_authenticated, Exception("Authorization token was not provided"))


def permission_required(perms: str) -> bool:
    def check_perms(user) -> bool:
        if isinstance(perms, str):
            return user.has_perms((perms,))
        return user.has_perms(perms)
    return user_passes_test(check_perms, Exception("Permission Denied"))
