import math
from collections import OrderedDict

class Fraction():
    numerator = 0
    denominator = 1
    sign = -1
    value = float(0/1)

    def __init__(self, fString):
        if fString == "":
            return

        parts = fString.split('/')
        if len(parts) != 2:
            raise Exception("Fraction has a numerator and denominator, formatted as a/b")

        self.numerator = int(parts[0])
        self.denominator = int(parts[1])

        if self.denominator == 0:
            raise Exception("Fraction %d/%d is indeterminate" % (self.numerator, self.denominator))

        if self.denominator < 0:
            self.denominator *= -1
            self.numerator *= -1

        self.value = float(self.numerator)/float(self.denominator)
        self.Simplify()

    def __add__(self, f):
        d = self.denominator * f.denominator
        n = self.numerator * f.denominator + self.denominator * f.numerator
        return Fraction("%d/%d" % (n, d))

    def __sub__(self, f):
        d = self.denominator * f.denominator
        n = self.numerator * f.denominator - self.denominator * f.numerator
        return Fraction("%d/%d" % (n, d))

    def __mul__(self, f):
        d = self.denominator * f.denominator
        n = self.numerator * f.numerator
        return Fraction("%d/%d" % (n, d))

    def __truediv__(self, f):
        d = self.denominator * f.numerator
        n = self.numerator * f.denominator
        return Fraction("%d/%d" % (n, d))

    def __lt__(self, f):
        return self.value < f.value

    def __le__(self, f):
        return self.value <= f.value

    def __gt__(self, f):
        return self.value > f.value

    def __ge__(self, f):
        return self.value >= f.value

    def __eq__(self, f):
        return self.value == f.value

    def Simplify(self):
        gcd = Fraction.GCD(self.numerator, self.denominator)
        self.numerator /= gcd
        self.denominator /= gcd

    def PrettyPrintFraction(self):
        print self.numerator,
        if self.denominator == 1:
            print
        else:
            print "/",
            print self.denominator

    @classmethod
    def PrimeFactors(cls, num):
        if num <= 0:
            raise Exception("Only numbers greater than 0 please")

        factors = []

        while num % 2 == 0:
            factors.append(2)
            num /= 2

        for i in range(3, int(math.sqrt(num))+1, 2):
            while num % i == 0:
                factors.append(i)
                num /= i

        if num != 1: factors.append(num)

        return factors

    @classmethod
    def LCM(cls, n1, n2):
        factors1 = Fraction.PrimeFactors(n1)
        factors2 = Fraction.PrimeFactors(n2)

        lcm = 1
        remaining = []
        for f in factors1:
            if f in factors2:
                lcm *= f
                factors2.remove(f)
            else:
                remaining.append(f)

        for f in factors2:
            lcm *= f

        for f in remaining:
            lcm *= f

        return lcm

    @classmethod
    def GCD(cls, n1, n2):
        factors1 = Fraction.PrimeFactors(n1)
        factors2 = Fraction.PrimeFactors(n2)

        commonFactor = 1
        for f in factors1:
            if f in factors2:
                commonFactor *= f
                factors2.remove(f)

        return commonFactor
