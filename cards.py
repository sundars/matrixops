from __future__ import print_function
import sys, random
from colors import bcolors

class Cards():
    deckSize = 52
    numSuits = 4
    cardsPerSuit = 13
    cards = []
    isOrdered = False
    numShuffles = 0
    correctGuesses = -1
    isValid = False

    def __init__(self):
        self.Reset()

    def Reset(self, __atype__="instanceobj, returns nothing - resets deck"):
        self.cards = []
        self.numSuits = 4
        self.cardsPerSuit = 13
        self.deckSize = self.numSuits * self.cardsPerSuit
        for i in range(0, self.numSuits):
            for j in range(0, self.cardsPerSuit):
                card = i*self.cardsPerSuit + j
                self.cards.append(card)

        self.isValid = True
        self.correctGuesses = -1
        self.numShuffles = 0
        self.isOrdered = True

    def Pop(self):
        card = self.cards[0]
        for i in range(1, self.deckSize):
            self.cards[i-1] = self.cards[i]

        self.cards[self.deckSize-1] = card

        return card

    def Test(self, __atype__="instanceobj, returns result of a guessing test"):
        if self.correctGuesses > -1:
            return self.correctGuesses

        self.correctGuesses = 0
        newDeck = Cards()
        seenCards = []
        card = newDeck.Pop()
        for i in range(0, self.deckSize):
            while card in seenCards:
                card = newDeck.Pop()

            if card == self.cards[i]:
                self.correctGuesses += 1

            seenCards.append(self.cards[i])

        return float(self.correctGuesses)

    def ShuffleAndTestMany(self, numShuffles=1, numTests=100, sType='Riffle', __atype__="instanceobj, int, int, str, returns result of a series of shuffles and series of test"):
        totalCorrect = 0
        for i in range(0, numTests):
            self.Reset()
            self.ShuffleMany(numShuffles, sType)
            totalCorrect += self.Test()

        return float(totalCorrect)/float(numTests)

    def ShuffleMany(self, numShuffles, sType='Riffle', __atype__="instanceobj, int, str, returns nothing but does many shuffles"):
        for i in range(0, numShuffles):
            self.Shuffle(sType)

        return

    def Shuffle(self, sType='Riffle', __atype__="instanceobj, str, returns nothing does a 'Riffle' 'Normal' or 'Perfect' shuffle"):
        if sType == 'Riffle':
            self.RiffleShuffle()

        elif sType == 'Perfect':
            self.PerfectShuffle()

        elif sType == 'Normal':
            self.NormalShuffle()

        else:
            self.RiffleShuffle()

        return

    def RiffleShuffle(self, __atype__="instanceobj, returns nothing does a 'Riffle' shuffle"):
        cut = random.randint(5, self.deckSize-5)
        left = self.cards[:cut]
        right = self.cards[cut:]

        if cut > 25:
            left = self.cards[cut:]
            right = self.cards[:cut]

        shufflePos = []
        for i in range(0, len(left)):
            pos = random.randint(0, len(right))
            while pos in shufflePos:
                pos = random.randint(0, len(right))

            shufflePos.append(pos)

        shufflePos.sort()
        newCards = []
        n = len(right)
        for i in range(0, n):
            if len(shufflePos) > 0 and i == shufflePos[0]:
                newCards.append(left.pop(0))
                newCards.append(right.pop(0))
                shufflePos.pop(0)

            else:
                newCards.append(right.pop(0))

        if len(left) == 1:
            newCards.append(left.pop(0))

        self.cards = newCards
        self.correctGuesses = -1
        self.isOrdered = False
        self.numShuffles += 1

        return

    def PerfectShuffle(self, __atype__="instanceobj, returns nothing does a 'Perfect' shuffle"):
        left = self.cards[:(self.deckSize/2)]
        right = self.cards[(self.deckSize/2):]

        newCards = []
        for i in range(0, self.deckSize/2):
            newCards.append(left.pop(0))
            newCards.append(right.pop(0))

        self.cards = newCards
        self.correctGuesses = -1
        self.isOrdered = False
        self.numShuffles += 1

        return

    def NormalShuffle(self, __atype__="instanceobj, returns nothing does a 'Normal' shuffle"):
        count = len(self.cards)
        cut1 = random.randint(1, self.deckSize-1)
        cut2 = random.randint(1, self.deckSize-1)
        while cut2 == cut1:
            cut2 = random.randint(1, self.deckSize-1)

        top = self.cards[:min(cut1, cut2)]
        middle = self.cards[min(cut1, cut2):max(cut1, cut2)]
        bottom = self.cards[max(cut1, cut2):]
        self.cards = middle + top + bottom

        self.correctGuesses = -1
        self.isOrdered = False
        self.numShuffles += 1

        return

    def PrettyPrint(self):
        suits = ['S', 'D', 'C', 'H']
        cards = [' A', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8', ' 9', '10', ' J', ' Q', ' K']

        for i in range(0, self.cardsPerSuit):
            print(" " + bcolors.B_DarkGray + bcolors.F_LightGray + "---------" + bcolors.END, end='')
            print(" " + bcolors.B_DarkGray + bcolors.F_LightGray + "---------" + bcolors.END, end='')
            print(" " + bcolors.B_DarkGray + bcolors.F_LightGray + "---------" + bcolors.END, end='')
            print(" " + bcolors.B_DarkGray + bcolors.F_LightGray + "---------" + bcolors.END)

            for j in range(0, self.numSuits):
                SI = int(self.cards[j * self.cardsPerSuit + i] / self.cardsPerSuit)
                CI = int(self.cards[j * self.cardsPerSuit + i] % self.cardsPerSuit)
                print(" " + bcolors.B_LightGray + bcolors.F_DarkGray + "|", end='')
                if SI == 0 or SI == 2:
                    color = bcolors.F_Black
                else:
                    color = bcolors.F_Red
                print(color + " {0:s}-{1:s} ".format(cards[CI], suits[SI]), end='')
                print(bcolors.F_DarkGray + " |" + bcolors.END, end='')
            print()

        print(" " + bcolors.B_LightGray + bcolors.F_DarkGray + "|       |" + bcolors.END, end='')
        print(" " + bcolors.B_LightGray + bcolors.F_DarkGray + "|       |" + bcolors.END, end='')
        print(" " + bcolors.B_LightGray + bcolors.F_DarkGray + "|       |" + bcolors.END, end='')
        print(" " + bcolors.B_LightGray + bcolors.F_DarkGray + "|       |" + bcolors.END)

        print(" " + bcolors.B_LightGray + bcolors.F_DarkGray + "|       |" + bcolors.END, end='')
        print(" " + bcolors.B_LightGray + bcolors.F_DarkGray + "|       |" + bcolors.END, end='')
        print(" " + bcolors.B_LightGray + bcolors.F_DarkGray + "|       |" + bcolors.END, end='')
        print(" " + bcolors.B_LightGray + bcolors.F_DarkGray + "|       |" + bcolors.END)

        for j in range(0, self.numSuits):
            SI = int(self.cards[j * self.cardsPerSuit + i] / self.cardsPerSuit)
            CI = int(self.cards[j * self.cardsPerSuit + i] % self.cardsPerSuit)
            print(" " + bcolors.B_LightGray + bcolors.F_DarkGray + "|", end='')
            if SI == 0 or SI == 2:
                color = bcolors.F_Black
            else:
                color = bcolors.F_Red
            print(color + " {0:s}-{1:s} ".format(cards[CI], suits[SI]), end='')
            print(bcolors.F_DarkGray + " |" + bcolors.END, end='')
        print()
        print(" " + bcolors.B_LightGray + bcolors.F_DarkGray + "|Pursute|" + bcolors.END, end='')
        print(" " + bcolors.B_LightGray + bcolors.F_DarkGray + "|Pursute|" + bcolors.END, end='')
        print(" " + bcolors.B_LightGray + bcolors.F_DarkGray + "|Pursute|" + bcolors.END, end='')
        print(" " + bcolors.B_LightGray + bcolors.F_DarkGray + "|Pursute|" + bcolors.END)

        print(" " + bcolors.B_DarkGray + bcolors.F_LightGray + "---------" + bcolors.END, end='')
        print(" " + bcolors.B_DarkGray + bcolors.F_LightGray + "---------" + bcolors.END, end='')
        print(" " + bcolors.B_DarkGray + bcolors.F_LightGray + "---------" + bcolors.END, end='')
        print(" " + bcolors.B_DarkGray + bcolors.F_LightGray + "---------" + bcolors.END)

        return

