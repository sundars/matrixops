from overrides import *
import sys, getopt
from cards import Cards
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
    useShuffleType = False
    useNumShuffles = False
    useNumTests = False

    print("Instance of class {0:s} is:".format(objectType))
    instance.PrettyPrint()

    while True:
        print('')
        print("Do any of the following to the object of class {0:s}...".format(objectType))
        method_list = [func for func in dir(klass) if callable(getattr(klass, func))
                            and not func.startswith("__")
                            and not func.startswith("Pop")]
        method_list.sort()
        for method in method_list:
            print("    {0:s}".format(method))
        print("    Exit")
        print('')
        command = print_raw_input(">>> ")

        if command == '':
            continue

        if command == 'Exit':
            return

        if command == "Shuffle" or command == 'ShuffleMany' or command == 'ShuffleAndTestMany':
            print('')
            print("Choose one of the following shuffle types - Riffle, Normal or Perfect - defaults to Riffle")
            shuffleType = print_raw_input("Shuffle type >>> ")
            if (shuffleType != 'Riffle' and shuffleType != 'Normal' and shuffleType != 'Perfect'):
                shuffleType = 'Riffle'

        if command == 'ShuffleMany' or command == 'ShuffleAndTestMany':
            print('')
            print("How many times would you like to shuffle the deck? - defaults to 1")
            try:
                numShuffles = int(print_raw_input("Number of shuffles >>> "))
                if numShuffles < 0 or numShuffles > 10000:
                    print("Number of shuffles {0:d} outside range (0,10000) - defaulting to 1".format(numShuffles))
                    numShuffles = 1

            except Exception as e:
                numShuffles = 1

        if command == 'ShuffleAndTestMany':
            print('')
            print("How many times would you like to test the shuffiliness of the deck? - defaults to 100")
            try:
                numTests = int(print_raw_input("Number of Tests >>> "))
                if numTests < 1 or numTests > 1000:
                    print("Number of shuffles {0:d} outside range (1,1000) - defaulting to 100".format(numTests))
                    numTests = 100

            except Exception as e:
                numTests = 100

        print_space()

        try:
            method_to_call = getattr(klass, command)

            if command == 'Test' or command == 'ShuffleAndTestMany':
                if command == 'ShuffleAndTestMany':
                    result = method_to_call(instance, numShuffles, numTests, shuffleType)
                    print("After shuffling with the {0:s} shuffle {1:d} times and running {2:d} tests".format(shuffleType, numShuffles, numTests))
                else:
                    result = method_to_call(instance)

                print("Number of cards correctly predicted in the shuffled deck is: {0:.2f}".format(result))
                print_space()

            elif command == 'ShuffleMany':
                    method_to_call(instance, numShuffles, shuffleType)

            elif command == 'Shuffle':
                    method_to_call(instance, shuffleType)

            elif command != 'PrettyPrint':
                method_to_call(instance)

            print_raw_input("After the operation <{0:s}>, to object {1:s} result is...".format(command, objectType))
            instance.PrettyPrint()

        except Exception as e:
            print(e)
            continue

    return

def print_space():
    print('')
    print("------------------------------------------------------------------------------------")

def print_raw_input(s):
    try:
        from builtins import input
        return input(s)
    except ImportError:
        return raw_input(s)

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
            print('Please provide a square matrix formatted as a11,a12,...,a1n,a21,a22,...,a2n,...,an1,an2,...,ann')
            marg = input(">>> ")

            instance = klass(marg, True)

        if (objectType == 'Equation'):
            print('Specify a system of equations to solve formatted as 2*a+3*b+1*c=4:5*a-1*c=1:...')
            sarg = input(">>> ")

            instance = klass(sarg, True)

        if (objectType == 'Fraction'):
            print('Specify a fraction formatted as a/b')
            farg = input(">>> ")

            instance = klass(farg)

        if (objectType == 'Cards'):
            instance = klass()

        return (instance, klass, objectType)
    except Exception as e:
        print(e)
        usage()

# Usage for this program
def usage():
    print('')
    print(sys.argv[0] + " [options]")
    print("Required:")
    print(" -c --class-type                     one of 'Matrix', 'Equation', 'Fraction' or 'Cards'")
    print("Options:")
    print(" -h, --help                          show this help message and exit")
    sys.exit(1)

main()
