from typing import Callable

from .Singleton import Singleton


class EventBus(Singleton):
    _handlers: dict[any, list[Callable]] = dict()

    def on(self, name: any, handler: Callable):
        if name not in self._handlers:
            self._handlers[name] = list()

        if handler not in self._handlers:
            self._handlers[name].append(handler)

    def once(self, name: any, handler: Callable):
        def _handler(*args, **kwargs):
            handler(*args, **kwargs)
            self.off(name, _handler)

        self.on(name, _handler)

    def emit(self, name: any, *args, **kwargs):
        if name in self._handlers:
            for h in self._handlers[name]:
                h(*args, **kwargs)

    def off(self, name: any, handler: Callable = None):
        if name not in self._handlers:
            return

        if handler is None:
            del self._handlers[name]
            return

        handlers = self._handlers[name]

        for h in handlers:
            if h is handler:
                handlers.remove(h)
                break

        if len(handlers) == 0:
            del self._handlers[name]
