try:
    import builtins as builtin
except Exception as e:
    import __builtin__ as builtin

# Override str
def str(number):
    if isinstance(number, float):
        return '{0:.2f}'.format(number)

    return builtin.str(number)
