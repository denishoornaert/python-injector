import unittest

from pythonInjector.src.lexer.struct import PythonEnvironment

from test import Configuration as config

class TestEnvironment(unittest.TestCase):

    """docstring for TestEnvironment."""

    def test_PythonEnvironment(self):
        environment = PythonEnvironment("out('17\\n')\nout('167\\n')\nout('1\\n')\n", '\t')
        expectation = "\t17\n\t167\n\t1\n\t\n"
        self.assertEqual(expectation, environment.execute())

    def test_PythonEnvironmentOperation(self):
        environment = PythonEnvironment("a = 42\nb = 25\nout(a-b)\n", '\t')
        expectation = "\t17\n"
        self.assertEqual(expectation, environment.execute())
