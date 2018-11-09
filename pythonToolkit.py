#Fun coercion and I/O utilities
def silentCoerce(coerceFunction=bool,value=None,deafultValue=None):
    "Eliminate coercion errors by returning a specified value if coercion fails."
    try:
        return coerceFunction(value)
    except:
        return deafultValue

def silentCheckForError(value):
    "Returns True if a variable exists, else returns false, no errors needed!"
    try:
        value
        return True
    except:
        return False


def typeinput(prompt="", coerceFunction=int, deafultValue=0):
    "Takes a input and returns only an a result of that type. deafultValue is value returned if coercion fails."
    return silentCoerce(coerceFunction,input(prompt),deafultValue)

def inputs(times=1, prompt="", coerceFunction=int, deafultValue=0):
    "Takes inputs and returns only an a result of that type (in a list). deafultValue is value returned if coercion throws an error."
    vals = []
    for _ in range(0,int(times)):
        vals.append(typeinput(prompt,coerceFunction,deafultValue))
    return vals

def finish():
    "Delays the termination of the python script interpreter."
    input("PRESS ENTER TO TERMINATE")