from typing import Callable


def singleton(class_: Callable) -> Callable:
    instance = None

    def fn(*args, **kwargs):
        nonlocal instance

        if instance is None:
            instance = class_(*args, **kwargs)

        return instance

    return fn
