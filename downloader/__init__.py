from .App import App

_app: App | None = None


def get_app() -> App:
    global _app
    if _app is None:
        _app = App()
    return _app
