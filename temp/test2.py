from inspect import getframeinfo, stack

def funcman():
    tucman()


def tucman():
    caller = getframeinfo(stack()[1][0])
    print(caller.filename, caller.lineno)