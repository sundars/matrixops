import math
from collections import OrderedDict

class Fraction():
    numerator = 0
    denominator = 1
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

        if self.numerator == 0:
            return

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

    def __div__(self, f):
        d = self.denominator * f.numerator
        n = self.numerator * f.denominator
        return Fraction("%d/%d" % (n, d))

    def __pow__(self, power):
        p = math.fabs(power)
        d = self.denominator ** p
        n = self.numerator ** p
        f = Fraction("%d/%d" % (n, d))

        if power < 0:
            return f.Reciprocal()

        return f

    def __lt__(self, f):
        try:
            return self.value < f.value
        except Exception, e:
            return self.value < f

    def __le__(self, f):
        try:
            return self.value <= f.value
        except Exception, e:
            return self.value <= f

    def __gt__(self, f):
        try:
            return self.value > f.value
        except Exception, e:
            return self.value > f

    def __ge__(self, f):
        try:
            return self.value >= f.value
        except Exception, e:
            return self.value >= f

    def __eq__(self, f):
        try:
            return self.value == f.value
        except Exception, e:
            return self.value == f

    def __ne__(self, f):
        try:
            return self.value != f.value
        except Exception, e:
            return self.value != f

    def __repr__(self):
        return self.FractionStr()

    def __str__(self):
        return self.FractionStr()

    def __float__(self):
        return self.value

    def __round__(self, n=0):
        return self

    def Reciprocal(self):
        return Fraction("%d/%d" % (self.denominator, self.numerator))

    def Simplify(self):
        gcd = Fraction.GCD(math.fabs(self.numerator), self.denominator)
        self.numerator /= gcd
        self.denominator /= gcd

    def PrettyPrintFraction(self):
        print self.numerator,
        if self.numerator == 0 or self.denominator == 1:
            print
        else:
            print "/",
            print self.denominator

    def FractionStr(self):
        s = "%d" % self.numerator
        if self.numerator != 0 and self.denominator != 1:
            s += "/"
            s += "%d" % self.denominator

        return s

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

    @classmethod
    def FromDecimal(cls, decimal):
        continuedFraction = []
        whole, remaining = (int(decimal), float("0.%s" % str(decimal)[(len(str(int(decimal)))+1):]))
        continuedFraction.append(whole)

        iter = 0
        while round(remaining,6) > 0.001 and iter < 16:
            reciprocal = 1/remaining
            whole, remaining = (int(reciprocal), float("0.%s" % str(reciprocal)[(len(str(int(reciprocal)))+1):]))
            continuedFraction.append(whole)
            iter += 1

        # Unpack the continued fraction
        pf = Fraction('0/1')
        for i in range(len(continuedFraction), 0, -1):
            if i == 1:
                return pf + continuedFraction[i-1]

            if i == len(continuedFraction):
                pf = Fraction("1/%d" % continuedFraction[i-1])

            else:
                pf = Fraction('1/1') / (pf + continuedFraction[i-1])
