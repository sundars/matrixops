from __future__ import print_function
from overrides import *
import sys, getopt, inspect
from cards import Cards
from hangman import Hangman
from fraction import Fraction
from matrix import Matrix
from equation import LinearEquations

def main():
    instance, klass, objectType = parseArgs()

    print("Entering interactive mode for object {0:s}".format(objectType))
    interactive(instance, klass, objectType)

    sys.exit(0)

# Interactive mode
def interactive(instance, klass, objectType):
    print("Instance of class {0:s} is:".format(objectType))
    instance.PrettyPrint()

    while True:
        print('')
        print("Do any of the following to the object of class {0:s}...".format(objectType))
        method_list = [func for func in dir(klass) if callable(getattr(klass, func))]
        method_list.sort()
        actionableMethods = []
        for method in method_list:
            methodArgs = ''
            try:
                method_to_call = getattr(klass, method)

                argNames = []
                try:
                    argNames = inspect.getfullargspec(method_to_call).args
                except Exception as e:
                    if sys.version_info[0] < 3:
                        argNames = inspect.getargspec(method_to_call).args

                if '__atype__' in argNames:
                    argTypes = []
                    try:
                        defaults = inspect.getfullargspec(method_to_call).defaults
                        argTypes = [arg.strip() for arg in defaults[len(defaults)-1].split(',')]
                    except Exception as e:
                        if sys.version_info[0] < 3:
                            defaults = inspect.getargspec(method_to_call).defaults
                            argTypes = [arg.strip() for arg in defaults[len(defaults)-1].split(',')]

                    methodArgs = '('
                    for argType in argTypes:
                        if argType not in ['classobj', 'instanceobj', 'staticobj'] and argType.find('returns') == -1:
                            methodArgs += argType.strip() + ','
                    if len(methodArgs) == 1:
                        methodArgs += ')'
                    else:
                        methodArgs = methodArgs[:-1] + ')'

                    print("    {0:s}{1:s}    ...".format(method, methodArgs), end='')
                    print(argTypes[len(argTypes)-1].rjust(100-len(methodArgs)-len(method)))
                    actionableMethods.append(method)

            except Exception as e:
                # ignore
                pass

        print("    Exit()    ...", end='')
        print("fairly obvious what this does".rjust(100-6))
        print('')
        actionableMethods.append('Exit')
        commandWithArgs = print_raw_input(">>> ")
        command = [c for c in commandWithArgs.split('(')][0]

        if command not in actionableMethods:
            continue

        if command == 'Exit':
            return

        try:
            method_to_call = getattr(klass, command)

            argTypes = []
            try:
                defaults = inspect.getfullargspec(method_to_call).defaults
                argTypes = [arg.strip() for arg in defaults[len(defaults)-1].split(',')]
            except Exception as e:
                if sys.version_info[0] < 3:
                    defaults = inspect.getargspec(method_to_call).defaults
                    argTypes = [arg.strip() for arg in defaults[len(defaults)-1].split(',')]

            args = [a.strip() for a in commandWithArgs[len(command)+1:-1].split(',')]

            hasReturnVal = True
            argvals = []
            loop = -1
            for argType in argTypes:
                if argType == 'classobj':
                    # do nothing
                    pass

                elif argType == 'instanceobj':
                    argvals.append(instance)

                elif argType == 'staticobj':
                    # do nothing
                    pass

                elif argType.find('returns') > -1:
                    if argType.find('nothing') > -1:
                        hasReturnVal = False

                else:
                    loop += 1
                    try:
                        if args[loop].find('[') > -1:
                            # Found a list
                            listType = argType.split(':')[1]
                            listval = [eval("{0:s}('{1:s}')".format(listType, args[loop].split('[')[1]))]

                            loop += 1
                            while args[loop].find(']') == -1:
                                listval.append(eval("{0:s}('{1:s}')".format(listType, args[loop])))
                                loop += 1

                            listval.append(eval("{0:s}('{1:s}')".format(listType, args[loop].split(']')[0])))
                            argvals.append(listval)

                        elif args[loop][:7] == 'Matrix(':
                            # Found a matrix string
                            s = args[loop][7:]

                            while args[loop].find(')') == -1:
                                loop += 1
                                if args[loop] != ':':
                                    s += ','
                                s += args[loop]

                            if s == args[loop][7:]:
                                s = args[loop][7:-1]
                            else:
                                s = s[:-1]

                            argvals.append(s)

                        else:
                            argvals.append(eval("{0:s}('{1:s}')".format(argType, args[loop])))

                    except Exception as e:
                        print(e)
                        continue

            returnval = method_to_call(*argvals)

            if hasReturnVal:
                if isinstance(returnval, klass):
                    print("{0:s} {1:s} and result is".format(commandWithArgs, argTypes[len(argTypes)-1]))
                    returnval.PrettyPrint()
                else:
                    print("{0:s} {1:s} and result is".format(commandWithArgs, argTypes[len(argTypes)-1]), returnval)

                print_raw_input("Press Enter to continue...")

            print_space()
            print("Current instance of class object {0:s} is".format(objectType))
            instance.PrettyPrint()

        except Exception as e:
            print(e)
            continue

    return

def print_space():
    print('')
    print("------------------------------------------------------------------------------------")

def parseArgs():
    objectType = ''

    # Get the inputs/arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hc:', ['--class-type'])
    except getopt.GetoptError:
        usage()

    # Parse the arguments
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-c', '--class-type'):
            objectType  = arg
        else:
            usage()

    try:
        if (objectType == ''):
            raise Exception("Required argument missing")
        
        klass = globals()[objectType]

        if (objectType == 'Matrix'):
            print("Please provide a square matrix formatted as 'Matrix(a11,a12,...,a1n,a21,a22,...,a2n,...,an1,an2,...,ann)'")
            marg = print_raw_input(">>> ")

            instance = klass(marg[7:-1], True)

        if (objectType == 'LinearEquations'):
            print("Specify a system of equations to solve formatted as 'LinearEquations(2*a+3*b+1*c=4:5*a-1*c=1:...)'")
            sarg = print_raw_input(">>> ")

            instance = klass(sarg[16:-1], True)

        if (objectType == 'Fraction'):
            print('Specify a fraction formatted as a/b')
            farg = print_raw_input(">>> ")

            instance = klass(farg, False)

        if (objectType == 'Hangman'):
            instance = klass(True)

        else:
            instance = klass()

        return (instance, klass, objectType)

    except KeyError:
        print("Unknown class:", objectType)
        usage()

    except Exception as e:
        print(e)
        usage()

def print_raw_input(s):
    try:
        from builtins import input
        return input(s)
    except ImportError:
        return raw_input(s)

# Usage for this program
def usage():
    print('')
    print(sys.argv[0] + " [options]")
    print("Required:")
    print(" -c --class-type                     one of 'Matrix', 'LinearEquations', 'Fraction', 'Cards' or 'Hangman'")
    print("Options:")
    print(" -h, --help                          show this help message and exit")
    sys.exit(1)

main()
