from cards import Cards
import sys, getopt

def main():
    deck, interactiveMode, runComparison, shuffleType, numShuffles = parseArgs()

    if interactiveMode:
        print("Entering interactive mode, all other arguments are ignored")
        interactive(deck, shuffleType, numShuffles, 100)

    elif runComparison:
        print("Running a comparison test on deck:")
        deck.PrettyPrint()
        print_space()
        print("How many shuffles of Normal, Riffle and Perfect should we do?")

        nCount = 1000
        try:
            nCount = int(print_raw_input("No. of Normal shuffles >> "))
        except Exception as e:
            print("Invalid input. Setting number of Normal shuffles to 1000")

        rCount = 7
        try:
            rCount = int(print_raw_input("No. of Riffle shuffles >> "))
        except Exception as e:
            print("Invalid input. Setting number of Riffle shuffles to 7")

        pCount = 100
        try:
            pCount = int(print_raw_input("No. of Perfect shuffles >> "))
        except Exception as e:
            print("Invalid input. Setting numnber of Perfect shuffles to 100")

        nResult = deck.ShuffleAndTestMany(nCount, 100, 'Normal')
        rResult = deck.ShuffleAndTestMany(rCount, 100, 'Riffle')
        pResult = deck.ShuffleAndTestMany(pCount, 100, 'Perfect')

        print_space()

        print("After {0:d} shuffles of Normal shuffle, number of cards correctly predicted on average is {1:.2f}".format(nCount, nResult))
        print("After {0:d} shuffles of Riffle shuffle, number of cards correctly predicted on average is {1:.2f}".format(rCount, rResult))
        print("After {0:d} shuffles of Perfect shuffle, number of cards correctly predicted on average is {1:.2f}".format(pCount, pResult))

    else:
        print("Running a {0:s} shuffle operation {1:d} times on deck:".format(shuffleType, numShuffles))
        deck.PrettyPrint()
        print_space()

        deck.ShuffleMany(numShuffles, shuffleType)

        print_raw_input("After the operation, deck is:...")
        deck.PrettyPrint()

        print_space()

    sys.exit(0)

# Interactive mode
def interactive(deck, shuffleType, numShuffles, numTests):
    useShuffleType = False
    useNumShuffles = False
    useNumTests = False

    print("A deck of cards fresh from the factory has arrived and it is sorted as below:")
    deck.PrettyPrint()

    while True:
        print('')
        print("Do any of the following to the deck...")
        method_list = [func for func in dir(Cards) if callable(getattr(Cards, func))
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

        method_to_call = getattr(Cards, command)

        if command == 'Test' or command == 'ShuffleAndTestMany':
            if command == 'ShuffleAndTestMany':
                result = method_to_call(deck, numShuffles, numTests, shuffleType)
                print("After shuffling with the {0:s} shuffle {1:d} times and running {2:d} tests".format(shuffleType, numShuffles, numTests))
            else:
                result = method_to_call(deck)

            print("Number of cards correctly predicted in the shuffled deck is: {0:.2f}".format(result))
            print_space()

        elif command == 'ShuffleMany':
                method_to_call(deck, numShuffles, shuffleType)

        elif command == 'Shuffle':
                method_to_call(deck, shuffleType)

        elif command != 'PrettyPrint':
            method_to_call(deck)

        print_raw_input("After the operation <{0:s}>, the deck of cards is now arranged as...".format(command))
        deck.PrettyPrint()

    return

def print_raw_input(s):
    try:
        from builtins import input
        return input(s)
    except ImportError:
        return raw_input(s)

def print_space():
    print('')
    print("------------------------------------------------------------------------------------")

def parseArgs():
    interactiveMode = False
    runComparison = False
    numShuffles = 1
    numShufflesStr = '1'
    shuffleType = 'Riffle'

    # Get the inputs/arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hics:n:', ['--shuffle-type', '--number-of-shuffles'])
    except getopt.GetoptError:
        usage()

    # Parse the arguments
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-i', '--interactive'):
            interactiveMode = True
        elif opt in ('-s', '--shuffle-type'):
            shuffleType = arg
        elif opt in ('-n', '--number-of-shuffles'):
            numShufflesStr = arg
        elif opt in ('-c', '--compare-shuffles'):
            runComparison  = True
        else:
            usage()

    try:
        deck = Cards()

        if (shuffleType != 'Riffle' and shuffleType != 'Normal' and shuffleType != 'Perfect'):
            raise Exception("Invalid shuffle type {0:s}".format(shuffleType))

        numShuffles = int(numShufflesStr)

        return (deck, interactiveMode, runComparison, shuffleType, numShuffles)
    except Exception as e:
        print(e)
        usage()

# Usage for this program
def usage():
    print('')
    print(sys.argv[0] + " [options]")
    print("Options:")
    print(" -i --interactive                    interactive mode")
    print(" -s --shuffle-type                   one of 'Normal', 'Riffle' or 'Perfect' - default: 'Riffle'")
    print(" -n --number-of-shuffles             number of shuffles - default: 1")
    print(" -c --compare-shuffles               compare effectiveness of the 3 shuffles")
    print(" -h, --help                          show this help message and exit")
    sys.exit(1)

main()
