import unittest

from src.lexer.Parser import Parser
from src.lexer.struct import Environment, PythonEnvironment, PlainTextEnvironment
from src.lexer.error import UnclosedEnvironmentError

from test import TestConfiguration as config

class TestParser(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        self.parser = None

    def test_CorrectParserInitalisation(self):
        filepath = config.getCompletePath("NoPythonEnvironment")
        self.parser = Parser(filepath)
        self.assertNotEqual(self.parser.content, "")
        self.assertEqual(self.parser.currentEnvironment, Environment.plainText)
        self.assertEqual(self.parser.cursor, 0)

    def test_isStateLatex(self):
        filepath = config.getCompletePath("NoPythonEnvironment")
        self.parser = Parser(filepath)
        self.parser.currentEnvironment = Environment.plainText
        self.assertTrue(self.parser.isStatePlainText())

    def test_UncorrectIsStateLatex(self):
        filepath = config.getCompletePath("NoPythonEnvironment")
        self.parser = Parser(filepath)
        self.parser.currentEnvironment = Environment.python
        self.assertFalse(self.parser.isStatePlainText())

    def test_NoPythonEnvironment(self):
        filepath = config.getCompletePath("NoPythonEnvironment")
        self.parser = Parser(filepath)
        res = self.parser.lex()
        self.assertEqual(res, PlainTextEnvironment(self.parser.content))

    def test_NothingElseToRead(self):
        filepath = config.getCompletePath("NoPythonEnvironment")
        self.parser = Parser(filepath)
        res = self.parser.lex()
        with self.assertRaises(EOFError):
            res = self.parser.lex()

    def test_OnePythonEnvironment(self):
        filepath = config.getCompletePath("OnePythonEnvironment")
        self.parser = Parser(filepath)
        res = self.parser.lex()
        self.assertEqual(res, PlainTextEnvironment("\documentclass[a4paper,11pt]{article}\n\\begin{document}\n\section{test}\n"))
        res = self.parser.lex()
        self.assertEqual(res, PythonEnvironment('print("Blablablablabla...")', ''))
        res = self.parser.lex()
        self.assertEqual(res, PlainTextEnvironment("\n\end{document}"))

    def test_UnclosedPythonEnvironment(self):
        filepath = config.getCompletePath("UnclosedPythonEnvironment")
        self.parser = Parser(filepath)
        res = self.parser.lex()
        with self.assertRaises(UnclosedEnvironmentError):
            res = self.parser.lex()

    def test_MultiplePythonEnvironments(self):
        filepath = config.getCompletePath("MultiplePythonEnvironments")
        self.parser = Parser(filepath)
        res = self.parser.lex()
        self.assertEqual(res, PlainTextEnvironment("\documentclass[a4paper,11pt]{article}\n\\begin{document}\n\section{test}\n"))
        res = self.parser.lex()
        self.assertEqual(res, PythonEnvironment('print("Blablablablabla...")', ''))
        res = self.parser.lex()
        self.assertEqual(res, PlainTextEnvironment('\nSome meaningful text\n'))
        res = self.parser.lex()
        self.assertEqual(res, PythonEnvironment('print("Almost the end...")', ''))
        res = self.parser.lex()
        self.assertEqual(res, PlainTextEnvironment("\n\end{document}"))

    def test_TwoConsecutivePythonEnvironments(self):
        filepath = config.getCompletePath("TwoConsecutivePythonEnvironments")
        self.parser = Parser(filepath)
        res = self.parser.lex()
        self.assertEqual(res, PlainTextEnvironment("\documentclass[a4paper,11pt]{article}\n\\begin{document}\n\section{test}\n"))
        res = self.parser.lex()
        self.assertEqual(res, PythonEnvironment('print("Bla")', ''))
        res = self.parser.lex()
        self.assertEqual(res, PlainTextEnvironment(''))
        res = self.parser.lex()
        self.assertEqual(res, PythonEnvironment('print("Bla")', ''))
        res = self.parser.lex()
        self.assertEqual(res, PlainTextEnvironment("\n\end{document}"))

    def test_MultilinePythonEnvironment(self):
        filepath = config.getCompletePath("MultilinePythonEnvironment")
        self.parser = Parser(filepath)
        res = self.parser.lex()
        self.assertEqual(res, PlainTextEnvironment("\documentclass[a4paper,11pt]{article}\n\\begin{document}\n\section{test}\n"))
        res = self.parser.lex()
        self.assertEqual(res, PythonEnvironment('a = 42\nb = 25\nout(a-b)', ''))
        res = self.parser.lex()
        self.assertEqual(res, PlainTextEnvironment("\n\end{document}"))

    def test_EmptyMultilinePythonEnvironment(self):
        filepath = config.getCompletePath("EmptyMultilinePythonEnvironment")
        self.parser = Parser(filepath)
        res = self.parser.lex()
        self.assertEqual(res, PlainTextEnvironment("\documentclass[a4paper,11pt]{article}\n\\begin{document}\n\section{test}\n"))
        res = self.parser.lex()
        self.assertEqual(res, PythonEnvironment('', ''))
        res = self.parser.lex()
        self.assertEqual(res, PlainTextEnvironment("\n\end{document}"))

if __name__ == '__main__':
    unittest.main()
