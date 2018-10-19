class Configuration():

    """docstring for Configuration."""

    latexTestFilePath = "test/src/assets/"

    pylatexExtension = ".ptex" # TODO modify this variable name

    @staticmethod
    def getCompletePath(filepath):
        res  = Configuration.latexTestFilePath # TODO modify this variable name
        res += filepath
        return  res + Configuration.pylatexExtension # TODO modify this variable name
