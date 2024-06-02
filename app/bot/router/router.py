from .dispatcher import MessageCommandHandler, CallBackCommandHandler

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable


class Router:
    messages = []
    callbacks = []

    def __init__(self, name: str = None):
        self.name = name

    def register_message(
        self,
        handler: 'Callable',
        name: str,
        dialog: str = None,
        with_args: bool = True,
        *args,
        **kwargs,
    ):
        self.messages.append(
            MessageCommandHandler(
                function=handler,
                name=name,
                dialog=dialog,
                with_args=with_args
            )
        )

    def register_callback(
        self,
        handler: 'Callable',
        name: str,
        *args, **kwargs,
    ):
        self.callbacks.append(
            CallBackCommandHandler(
                function=handler,
                name=name,
            )
        )

    def message(
        self,
        names: str | list,
        dialog: str = None,
        with_args: bool = True,
        *args,
        **kwargs,
    ) -> 'Callable':
        def decorator(function) -> 'Callable':
            names_list = names

            if not isinstance(names, list):
                names_list = [names]

            for name in names_list:
                self.register_message(
                    function, name, dialog,
                    with_args, *args, **kwargs
                )

            return function

        return decorator

    def callback(
        self,
        name: str | list,
        *args, **kwargs,
    ) -> 'Callable':
        def decorator(function) -> 'Callable':
            self.register_callback(
                function, name,
                *args, **kwargs
            )

            return function

        return decorator
