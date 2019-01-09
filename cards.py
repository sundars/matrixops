import random

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

    def Reset(self):
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

    def Test(self):
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

    def ShuffleAndTestMany(self, numShuffles=1, numTests=100, sType='Riffle'):
        totalCorrect = 0
        for i in range(0, numTests):
            self.Reset()
            self.ShuffleMany(numShuffles, sType)
            totalCorrect += self.Test()

        return float(totalCorrect)/float(numTests)

    def ShuffleMany(self, numShuffles, sType='Riffle'):
        for i in range(0, numShuffles):
            self.Shuffle(sType)

        return

    def Shuffle(self, sType='Riffle'):
        if sType == 'Riffle':
            self.RiffleShuffle()

        elif sType == 'Perfect':
            self.PerfectShuffle()

        elif sType == 'Normal':
            self.NormalShuffle()

        else:
            self.RiffleShuffle()

        return

    def RiffleShuffle(self):
        cut = random.randint(3*self.deckSize/8, 5*self.deckSize/8)
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

    def PerfectShuffle(self):
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

    def NormalShuffle(self):
        count = len(self.cards)
        cut = random.randint(3*count/8, 5*count/8)
        remaining = self.cards
        newCards = []
        loop = 0
        while loop < 2 and cut > 0:
            newCards = remaining[:cut] + newCards
            remaining = remaining[cut:]
            count = len(remaining)
            cut = random.randint(3*count/8, 5*count/8)
            loop += 1
        newCards = remaining + newCards

        self.cards = newCards
        self.correctGuesses = -1
        self.isOrdered = False
        self.numShuffles += 1

        return

    def PrettyPrint(self):
        suits = ['S', 'D', 'C', 'H']
        cards = [' A', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8', ' 9', '10', ' J', ' Q', ' K']

        for i in range(0, self.cardsPerSuit):
            print " _________  _________  _________  _________ "
            for j in range(0, self.numSuits):
                suitIndex = self.cards[j * self.cardsPerSuit + i] / self.cardsPerSuit
                cardIndex = self.cards[j * self.cardsPerSuit + i] % self.cardsPerSuit
                print " | %s-%s  |" % (cards[cardIndex], suits[suitIndex]),
            print
        print " |       |  |       |  |       |  |       | "
        print " |       |  |       |  |       |  |       | "
        print " ---------  ---------  ---------  --------- "

        return

