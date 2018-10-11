import os
from src.fileController import FileController
from src.lexer import Parser
from src.lexer.struct import Environment
from src.interpreter import Interpreter

class Generator():

    """docstring for Generator."""

    @staticmethod
    def generates(srcFile, extension):
        # Setup variables
        parser = Parser(srcFile)
        data = ""
        # Main part of the code
        try:
            while(True):
                res = parser.lex()
                if(res[0] == Environment.python):
                    data += Interpreter.execute(res[1])
                else:
                    data += res[1]
        except EOFError as e:
            pass #resume ; typically acts as a break
        # End of the process : write the generated LaTeX file
        destFile = os.path.splitext(srcFile)[0]+"."+extension
        FileController.write(destFile, data)
