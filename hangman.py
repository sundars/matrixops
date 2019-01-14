from __future__ import print_function
from colors import bcolors
import random

class Hangman:
    allWords = []
    wordInPlay = []
    guessedsoFar = []
    numberCorrect = 0
    numberAttempted = 0
    lettersUsed = []

    def __init__(self):
        try:
            with open('/usr/share/dict/words', 'r') as dictionary:
                self.allWords = [line.strip() for line in dictionary]

            randomPos = random.randint(0, len(self.allWords))
            if len(self.allWords[randomPos]) < 7:
                randomPos = random.randint(0, len(self.allWords))

            self.wordInPlay = list(self.allWords[randomPos].lower())
            self.guessedSoFar = []
            for i in range(0, len(self.wordInPlay)):
                self.guessedSoFar.append(' ')

            self.lettersUsed = []
            self.numberAttempted = 0
            self.numberCorrect = 0

        except Exception as e:
            print(e)

    def GuessLetter(self, s, __atype__='instanceobj, str, checks if letter exists and returns nothing'):
        s = s.lower()
        if len(s) != 1:
            raise Exception("Guess only one letter at a time, please")

        if s in self.lettersUsed:
            raise Exception("You have already guessed this letter, try another one")

        self.numberAttempted += 1
        self.lettersUsed.append(s)
        self.lettersUsed.sort()

        if s in self.wordInPlay:
            self.numberCorrect += 1

        updatePositions = [i for i,x in enumerate(self.wordInPlay) if x == s]

        for i in range(0, len(updatePositions)):
            assert (self.guessedSoFar[updatePositions[i]] == ' '), "Something went wrong here..."
            self.guessedSoFar[updatePositions[i]] = s

        for i in range(0, len(self.wordInPlay)):
            if self.guessedSoFar[i] != self.wordInPlay[i]:
                return

        self.PrintCorrect()
        self.GetNewWord()
        self.PrettyPrint()

    def GuessWord(self, w, __atype__='instanceobj, str, checks if word is right and returns nothing'):
        word = list(w.lower())
        if len(word) != len(self.wordInPlay):
            raise Exception("Sorry, your guess is wrong")

        for i in range(0, len(word)):
            if word[i] != self.wordInPlay[i]:
                raise Exception("Sorry, your guess is wrong")

        self.PrintCorrect()
        self.GetNewWord()
        self.PrettyPrint()

    def PrintCorrect(self):
        print("")
        print("")
        print("---------------------------------")
        print("           You got it!           ")
        print("---------------------------------")
        print("")
        print("")

    def GetNewWord(self):
        try:
            randomPos = random.randint(0, len(self.allWords))
            if len(self.allWords[randomPos]) < 7:
                randomPos = random.randint(0, len(self.allWords))

            self.wordInPlay = list(self.allWords[randomPos].lower())
            self.guessedSoFar = []
            for i in range(0, len(self.wordInPlay)):
                self.guessedSoFar.append(' ')

            self.lettersUsed = []
            self.numberAttempted = 0
            self.numberCorrect = 0

        except Exception as e:
            print(e)

    def PrettyPrint(self):
        hangPos = self.numberAttempted - self.numberCorrect

        # Print basic stuff
        print("  _________")
        print("  |        |", end='')

        print("               Word so far: ", end='')
        for i in range(0, len(self.guessedSoFar)):
            print(bcolors.UNDERLINE + self.guessedSoFar[i] + bcolors.ENDC, end='')
            print(' ', end='')
        print('')

        print("  |        |")
        print("  |        |", end='')

        print("               Letters used so far: ", end='')
        print(self.lettersUsed)

        if hangPos > 0:
            print("  |    ____|____")

            if hangPos > 1:
                print("  |    | o   o |")
            else:
                print("  |    |       |")

            if hangPos > 2:
                print("  |    |   v   |")
            else:
                print("  |    |       |")

            if hangPos > 3:
                print("  |    |  ---  |")
            else:
                print("  |    |       |")

            print("  |    ---------")

            if hangPos > 4:
                print("  |       | |")
                print("  |       | |")
            else:
                print("  |          ")
                print("  |          ")

            if hangPos > 5:
                print("  |     /-| |-\\")
                print("  |   /   | |  \\")

            elif hangPos > 4:
                print("  |       | |")
                print("  |       | |")
            else:
                print("  |          ")
                print("  |          ")

            if hangPos > 4:
                print("  |       | |")
                print("  |       | |")
            else:
                print("  |          ")
                print("  |          ")

            if hangPos > 6:
                print("  |      /   \\")
                print("  |     /     \\")
                print("  |    /       \\")
            else:
                print("  |")
                print("  |")
                print("  |")

        else:
            print("  |")
            print("  |")
            print("  |")
            print("  |")
            print("  |")
            print("  |")
            print("  |")
            print("  |")
            print("  |")
            print("  |")
            print("  |")
            print("  |")
            print("  |")
            print("  |")

        print("  |")
        print("  |")
        print("  |_______________")

        if hangPos > 6:
            print("")
            print("")
            print("---------------------------------------------------------------")
            print("Sorry, you have been hung out to dry! The word is " + bcolors.BOLD, end='')
            for i in range(0, len(self.wordInPlay)):
                print(self.wordInPlay[i],end='')
            print(bcolors.ENDC)
            print("---------------------------------------------------------------")
            print("")
            print("")

            self.GetNewWord()
            self.PrettyPrint()
