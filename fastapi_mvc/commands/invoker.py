"""FastAPI MVC Invoker class implementation.

The fastapi-mvc.commands submodule implements command design pattern:
https://refactoring.guru/design-patterns/command
"""
import logging

from fastapi_mvc.commands import Command


class Invoker(object):
    """"""
    __slots__ = (
        "_log",
        "_on_start",
        "_on_finish",
    )

    def __init__(self):
        """"""
        self._log = logging.getLogger(self.__class__.__name__)
        self._log.debug("Initialize Invoker class object instance.")
        self._on_start = None
        self._on_finish = None

    @property
    def on_start(self):
        return self._on_start

    @on_start.setter
    def on_start(self, value):
        self._on_start = value

    @property
    def on_finish(self):
        return self._on_finish

    @on_finish.setter
    def on_finish(self, value):
        self._on_finish = value

    def execute(self):
        """"""
        if isinstance(self._on_start, Command):
            self._on_start.execute()

        if isinstance(self._on_finish, Command):
            self._on_finish.execute()