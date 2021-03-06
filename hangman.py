from __future__ import print_function
from colors import bcolors
from word import Oxford
from pause import Pause
import random

class Hangman:
    allWords = []
    wordInPlay = []
    guessedSoFar = []
    numberCorrect = 0
    numberAttempted = 0
    lettersUsed = []
    useOxford = False
    oxford = None

    def __init__(self, useOxford=False):
        try:
            if not useOxford:
                self.useOxford = useOxford
                with open('/usr/share/dict/words', 'r') as dictionary:
                    self.allWords = [line.strip() for line in dictionary]

                randomPos = random.randint(0, len(self.allWords))
                if len(self.allWords[randomPos]) < 7:
                    randomPos = random.randint(0, len(self.allWords))

                self.wordInPlay = list(self.allWords[randomPos].lower())

            else:
                self.useOxford = useOxford
                self.oxford = Oxford()
                self.wordInPlay = self.oxford.GetWord()

            self.guessedSoFar = []
            for i in range(0, len(self.wordInPlay)):
                self.guessedSoFar.append(' ')

            self.lettersUsed = []
            self.numberAttempted = 0
            self.numberCorrect = 0

        except Exception as e:
            print(e)

    def GuessLetter(self, s, __atype__='instanceobj, str, checks if letter exists and returns'):
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
                hangPos = self.numberAttempted - self.numberCorrect
                if hangPos > 6:
                    self.PrettyPrint()
                    return Pause()

                return None

        self.PrintCorrect()
        self.GetNewWord()
        return Pause()

    def GuessWord(self, w, __atype__='instanceobj, str, checks if word is right and returns'):
        self.numberAttempted = self.numberCorrect + 7
        word = list(w.lower())
        if len(word) != len(self.wordInPlay):
            self.PrettyPrint()
            return Pause()

        for i in range(0, len(word)):
            if word[i] != self.wordInPlay[i]:
                self.PrettyPrint()
                return Pause()

        self.PrintCorrect()
        self.GetNewWord()
        return Pause()

    def PrintCorrect(self):
        print("")
        print("")
        print("------------------------------------------------------------------------------------")
        print("  You got it!")
        print("  The word is " + bcolors.BOLD, end='')
        for i in range(0, len(self.wordInPlay)):
            print(self.wordInPlay[i],end='')
        print(bcolors.ENDC)
        if self.useOxford:
            entry = '{0:s}'.format(self.oxford.GetEntry())
            if len(entry) > 80:
                words = entry.split(' ')
                print(bcolors.ITALIC, end='')
                i = 0
                while i < len(words):
                    print('  ' + words[i],end='')
                    length = len(words[i]) + 2
                    while i < len(words)-1 and length+len(words[i+1])+1 < 80:
                        i += 1
                        print(' ' + words[i], end='')
                        length += len(words[i]) + 1
                    print('')
                    i += 1
                print(bcolors.ENDC,end='')
            else:
                print(bcolors.ITALIC + '  ' + entry + bcolors.ENDC)
        print("------------------------------------------------------------------------------------")
        print("")
        print("")

    def PrintWrong(self):
        print("")
        print("")
        print("------------------------------------------------------------------------------------")
        print("  Sorry, you have been hung out to dry!")
        print("  The word is " + bcolors.BOLD, end='')
        for i in range(0, len(self.wordInPlay)):
            print(self.wordInPlay[i],end='')
        print(bcolors.ENDC)
        if self.useOxford:
            entry = '{0:s}'.format(self.oxford.GetEntry())
            if len(entry) > 80:
                words = entry.split(' ')
                print(bcolors.ITALIC, end='')
                i = 0
                while i < len(words):
                    print('  ' + words[i],end='')
                    length = len(words[i]) + 2
                    while i < len(words)-1 and length+len(words[i+1])+1 < 80:
                        i += 1
                        print(' ' + words[i], end='')
                        length += len(words[i]) + 1
                    print('')
                    i += 1
                print(bcolors.ENDC,end='')
            else:
                print(bcolors.ITALIC + '  ' + entry + bcolors.ENDC)
        print("------------------------------------------------------------------------------------")
        print("")
        print("")

    def GetNewWord(self, __atype__='instanceobj, resets the word and starts game again returns nothing'):
        try:
            if not self.useOxford:
                randomPos = random.randint(0, len(self.allWords))
                if len(self.allWords[randomPos]) < 7:
                    randomPos = random.randint(0, len(self.allWords))

                self.wordInPlay = list(self.allWords[randomPos].lower())

            else:
                self.wordInPlay = self.oxford.GetWord()

            self.guessedSoFar = []
            for i in range(0, len(self.wordInPlay)):
                self.guessedSoFar.append(' ')

            self.lettersUsed = []
            self.numberAttempted = 0
            self.numberCorrect = 0

        except Exception as e:
            print(e)

    def ChangeCategory(self, category='', __atype__='instanceobj, str, changes word category and starts game again returns nothing'):
        if not self.useOxford:
            return

        category = self.oxford.ChangeCategory(category)
        self.GetNewWord()

    def PrettyPrint(self):
        hangPos = self.numberAttempted - self.numberCorrect

        # Print basic stuff
        print("  _________")
        print("  |        |", end='')
        if not self.useOxford:
            print("               Not using Oxford APIs, so category is random and cannot be changed")
        else:
            print("               Word category is: {0:s}".format(self.oxford.GetCategory()))

        print("  |        |")
        print("  |        |", end='')
        print("               Word so far: ", end='')
        for i in range(0, len(self.guessedSoFar)):
            print(bcolors.UNDERLINE + self.guessedSoFar[i] + bcolors.ENDC, end='')
            print(' ', end='')
        print(' ({0:d} letters)'.format(len(self.wordInPlay)), end='')
        print('')

        if hangPos > 0:
            print("  |    ____|____", end='')
            print("           Letters used so far: ", end='')
            print(self.lettersUsed)

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
            print("  |",end='')
            print("                        Letters used so far: ", end='')
            print(self.lettersUsed)

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
            self.PrintWrong()
            self.GetNewWord()
