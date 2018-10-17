from pythonInjector.src.lexer.struct import Environment
from pythonInjector.src.lexer.error import UnclosedEnvironmentError, PatternNotFoundError, InlineEnvironmentError, MultilineEnvironmentError
from pythonInjector.src.fileController import FileController

class Parser():

    """docstring for Parser."""

    def __init__(self, filename):
        self.content = FileController.read(filename)
        self.currentEnvironment = Environment.latex
        self.cursor = 0

    def isStateLatex(self):
        """
        (public) Returns whether the previous environment was LaTex or Python.
        """
        return self.currentEnvironment == Environment.latex

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

    def multilineFormating(self, string):
        prefix = ""
        counter = 0
        state = 0
        while(counter < len(string)):
            if(string[counter] == '\n'):
                print("WARNING : ill-formed multiline environment ! There is an extra '\\n'.")
                string = string[counter+1:] # remove the useless blank chars
                prefix = "" # reset
                counter = 0
            elif(string[counter] in (' ', '\n')):
                prefix += string[counter]
                counter += 1
            else:
                break

        string = string.split('\n')
        if(all([s in (' ', '\t') for s in string[len(string)-1]])):
            string = string[:len(string)-1] # remove last element
        else:
            raise MultilineEnvironmentError("The multiline python environment is not correctly closed. Have you finished the environment by a '\\n' followed by a sequence of blank chars ?")
        string = '\n'.join([line if(line == '') else line[len(prefix):] for line in string])

#        while(counter < len(string)):
#            if(string[counter] == '\n'):
#                print("WARNING : ill-formed multiline environment ! There is an extra '\\n'.")
#                string = string[counter+1:] # remove the useless blank chars
#                prefix = "" # reset
#                counter = -1
#            elif(string[counter] in (' ', '\t')):
#                prefix += string[counter]
#            else: # first char found
#                string = string.split('\n')
#                if(all([s in (' ', '\t') for s in string[len(string)-1]])):
#                    string = string[:len(string)-1] # remove last element
#                else:
#                    raise MultilineEnvironmentError("The multiline python environment is not correctly closed. Have you finished the environment by a '\\n' followed by a sequence of blank chars ?")
#                string = '\n'.join([line if(line == '') else line[len(prefix):] for line in string])
#            counter += 1
        return string

    def pythonEnvironmentFormating(self, string):
        res = ""
        counter = 0
        while(counter < len(string)):
            if(string[counter] == '\n'):
                res = self.multilineFormating(string[counter:])
                break
            elif(string[counter] != '\t' and string[counter] != ' '):
                print(string[counter:])
                res = self.inlineFormating(string[counter:])
                break
            # else: keep looping
            counter += 1
        return res

    def manageNewEnvironment(self, index, delimiter):
        """
        (private) Returns a tuple of the environment and its associated content.
        In addition, the method manages correctly the object attributs.
        """
        res = None
        if(index >= 0):
            if(self.isStateLatex()):
                res = (Environment.latex, self.content[self.cursor:index])
            else:
                # res = (Environment.python, self.content[self.cursor:index].strip())
                instructions = self.pythonEnvironmentFormating(self.content[self.cursor:index])
                res = (Environment.python, instructions)
            self.cursor = index+len(delimiter)
            self.currentEnvironment = Environment.python if(self.isStateLatex()) else Environment.latex
        return res

    def manageEndEnvironment(self, delimiter):
        """
        (private) Returns a tuple of the environment and its associated content
        or raises an error if it appears that the python environment has not
        been closed (i.e. if no '?>' appears in the remaing input).
        """
        res = None
        if(delimiter == "<?"): # and index == -1 : the remaining of the file only contains latex environment
            res = (Environment.latex, self.content[self.cursor:])
            self.currentEnvironment = Environment.latex
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
            delimiter = "<?" if(self.isStateLatex()) else "?>"
            try:
                index = self.indexOf(delimiter, self.cursor)
                res = self.manageNewEnvironment(index, delimiter)
            except PatternNotFoundError as e:
                res = self.manageEndEnvironment(delimiter)
        else:
            raise EOFError()
        return res
