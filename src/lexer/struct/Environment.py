from enum import Enum
from pythonInjector.src.interpreter import Interpreter

class Environment(Enum):
    python = 0
    plainText = 1


class PythonEnvironment():

    """docstring for PythonEnvironment."""

    def __init__(self, content, prefix):
        self.content = content
        self.prefix = prefix

    def __eq__(self, other):
        return (self.content == other.content) and (self.prefix == other.prefix)

    def execute(self):
        return Interpreter.execute(self.content)


class PlainTextEnvironment():

    """docstring for PlainTextEnvironment."""

    def __init__(self, content):
        self.content = content

    def __eq__(self, other):
        return (self.content == other.content)

    def execute(self):
        return self.content
