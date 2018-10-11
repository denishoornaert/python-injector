# Collection of the PyLaTeX built-in functions

def out(objectToSerialise):
    try:
        string = objectToSerialise.__out__()
    except AttributeError as e:
        string = objectToSerialise.__str__()
    print(string, end='')
