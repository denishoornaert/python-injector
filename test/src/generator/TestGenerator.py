import unittest

from pythonInjector.src.generator import Generator

from test import Configuration as config

class TestGenerator(unittest.TestCase):

    """docstring for TestGenerator."""

    def test_FullInterpretation(self):
        expectedTextFile = open(config.getCompletePath("ExpectedOutput"), 'r')
        expectedText = expectedTextFile.read()
        expectedTextFile.close()
        Generator.generates(config.getCompletePath("ConcreteTest"), "out")
        processedTextFile = open(config.latexTestFilePath+"ConcreteTest"+".out")
        processedText = processedTextFile.read()
        processedTextFile.close()
        self.assertEqual(expectedText, processedText)
