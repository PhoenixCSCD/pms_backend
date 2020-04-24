from functools import wraps


def user_passes_test(test, exception: Exception = None):
    def decorator(func):
        @wraps(func)
        def wrapper(root, info, *args, **kwargs):
            if test(info.context.user):
                return func(root, info, *args, **kwargs)

            if exception is not None:
                raise exception
        return wrapper

    return decorator


def login_required():
    return user_passes_test(lambda user: user.is_authenticated, Exception("Authorization token was not provided"))


def permission_required(perms: str):
    def check_perms(user) -> bool:
        if isinstance(perms, str):
            return user.has_perms((perms,))
        return user.has_perms(perms)
    return user_passes_test(check_perms, Exception("Permission Denied"))
