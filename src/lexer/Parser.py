from pythonInjector.src.lexer.struct import Environment, PlainTextEnvironment, PythonEnvironment
from pythonInjector.src.lexer.error import UnclosedEnvironmentError, PatternNotFoundError, InlineEnvironmentError, MultilineEnvironmentError
from pythonInjector.src.fileController import FileController

class Parser():

    """docstring for Parser."""

    def __init__(self, filename = ''):
        self.content = FileController.read(filename)
        self.currentEnvironment = Environment.plainText
        self.cursor = 0

    def isStatePlainText(self):
        """
        (public) Returns whether the previous environment was PlainText or Python.
        """
        return self.currentEnvironment == Environment.plainText

    def indexOf(self, pattern, start=0):
        """
        (private) Returns the index of 'pattern' in 'self.content' from a
        specific start. If the pattern is not found, an error is raised.
        """
        index = self.content[start:].find(pattern)
        if(index >= 0):
            index += start
        else: # index == -1
            raise PatternNotFoundError("The pattern '"+pattern+"' has not been found")
        return index

    def inlineFormating(self, string):
        if(string.count('\n')):
            raise InlineEnvironmentError("The inline python environment contains a '\\n'. Try to create a multiline python environment.")
        return string

    def getBlankCharsOnLeft(self, string):
        prefix = ""
        counter = 0
        while(counter < len(string)):
            if(string[counter] in (' ', '\t')):
                prefix += string[counter]
                counter += 1
            else:
                counter = len(string)
        return prefix

    def multilineFormating(self, string):
        strings = string.split('\n')
        cleanedStrings = [string for string in strings if(not(all([s in (' ', '\t') for s in string])))]
        prefix = self.getBlankCharsOnLeft(cleanedStrings[0]) if (len(cleanedStrings) > 0) else ""
        string = '\n'.join([line if(line == '') else line[len(prefix):] for line in cleanedStrings])
        return string, prefix

    def pythonEnvironmentFormating(self, string):
        res = ""
        prefix = ""
        counter = 0
        while(counter < len(string)):
            if(string[counter] == '\n'):
                res, prefix = self.multilineFormating(string[counter:])
                break
            elif(string[counter] != '\t' and string[counter] != ' '):
                res = self.inlineFormating(string[counter:])
                break
            # else: keep looping
            counter += 1
        return res, prefix

    def manageNewEnvironment(self, index, delimiter):
        """
        (private) Returns a tuple of the environment and its associated content.
        In addition, the method manages correctly the object attributs.
        """
        res = None
        if(index >= 0):
            if(self.isStatePlainText()):
                res = PlainTextEnvironment(self.content[self.cursor:index])
                self.currentEnvironment = Environment.python
            else:
                instructions, prefix = self.pythonEnvironmentFormating(self.content[self.cursor:index])
                res = PythonEnvironment(instructions, prefix)
                self.currentEnvironment = Environment.plainText
            self.cursor = index+len(delimiter)
        return res

    def manageEndEnvironment(self, delimiter):
        """
        (private) Returns a tuple of the environment and its associated content
        or raises an error if it appears that the python environment has not
        been closed (i.e. if no '?>' appears in the remaing input).
        """
        res = None
        if(delimiter == "<?"): # and index == -1 : the remaining of the file only contains plainText environment
            res = PlainTextEnvironment(self.content[self.cursor:])
            self.currentEnvironment = Environment.plainText
            self.cursor = len(self.content)-1
        else: # delimiter == "?>" and index == -1 : the python environment is not closed
            raise UnclosedEnvironmentError("The Python environment openned at (x, y) is not closed.")
        return res

    def lex(self):
        """
        (public) Returns a tuple contaning the detected environment and its content. Will
        eventually raise an error when reaching the end of the file.
        """
        res = None
        if(self.cursor < len(self.content)-1):
            delimiter = "<?" if(self.isStatePlainText()) else "?>"
            try:
                index = self.indexOf(delimiter, self.cursor)
                res = self.manageNewEnvironment(index, delimiter)
            except PatternNotFoundError as e:
                res = self.manageEndEnvironment(delimiter)
        else:
            raise EOFError()
        return res
