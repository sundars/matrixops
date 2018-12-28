import __builtin__

# Override str
def str(number):
    if isinstance(number, float):
        return '%.2f' % number

    return __builtin__.str(number)
