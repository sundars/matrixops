from __future__ import print_function
import math
from collections import OrderedDict
from pause import Pause

class Fraction:
    numerator = 0
    denominator = 1
    value = float(0/1)

    def __init__(self, fString, simplify=True):
        if fString == "":
            return

        parts = fString.split('/')
        if len(parts) != 2:
            raise Exception("Fraction has a numerator and denominator, formatted as a/b")

        self.numerator = int(parts[0])
        self.denominator = int(parts[1])

        if self.denominator == 0:
            raise Exception("Fraction {0:d}/{1:d} is indeterminate".format(self.numerator, self.denominator))

        if self.numerator == 0:
            return

        if self.denominator < 0:
            self.denominator *= -1
            self.numerator *= -1

        self.value = float(self.numerator)/float(self.denominator)
        if simplify:
            self.Simplify()

    def __add__(self, f, __atype__="instanceobj, Fraction, returns a fraction"):
        d = self.denominator * f.denominator
        n = self.numerator * f.denominator + self.denominator * f.numerator
        return Fraction("{0:d}/{1:d}".format(int(n), int(d)))

    def __sub__(self, f, __atype__="instanceobj, Fraction, returns a fraction"):
        d = self.denominator * f.denominator
        n = self.numerator * f.denominator - self.denominator * f.numerator
        return Fraction("{0:d}/{1:d}".format(int(n), int(d)))

    def __mul__(self, f, __atype__="instanceobj, Fraction, returns a fraction"):
        d = self.denominator * f.denominator
        n = self.numerator * f.numerator
        return Fraction("{0:d}/{1:d}".format(int(n), int(d)))

    def __div__(self, f, __atype__="instanceobj, Fraction, returns a fraction"):
        d = self.denominator * f.numerator
        n = self.numerator * f.denominator
        return Fraction("{0:d}/{1:d}".format(int(n), int(d)))

    def __truediv__(self, f, __atype__="instanceobj, Fraction, returns a fraction"):
        d = self.denominator * f.numerator
        n = self.numerator * f.denominator
        return Fraction("{0:d}/{1:d}".format(int(n), int(d)))

    def __pow__(self, power, __atype__="instanceobj, int, returns a fraction"):
        p = math.fabs(power)
        fd = Fraction.FromDecimal(self.denominator ** p)
        fn = Fraction.FromDecimal(self.numerator ** p)
        if power < 0:
            return fd / fn

        return fn / fd

    def __lt__(self, f, __atype__="instanceobj, Fraction, returns a boolean"):
        try:
            return self.value < f.value
        except Exception as e:
            return self.value < f

    def __le__(self, f, __atype__="instanceobj, Fraction, returns a boolean"):
        try:
            return self.value <= f.value
        except Exception as e:
            return self.value <= f

    def __gt__(self, f, __atype__="instanceobj, Fraction, returns a boolean"):
        try:
            return self.value > f.value
        except Exception as e:
            return self.value > f

    def __ge__(self, f, __atype__="instanceobj, Fraction, returns a boolean"):
        try:
            return self.value >= f.value
        except Exception as e:
            return self.value >= f

    def __eq__(self, f, __atype__="instanceobj, Fraction, returns a boolean"):
        try:
            return self.value == f.value
        except Exception as e:
            return self.value == f

    def __ne__(self, f, __atype__="instanceobj, Fraction, returns a boolean"):
        try:
            return self.value != f.value
        except Exception as e:
            return self.value != f

    def __repr__(self):
        return self.FractionStr()

    def __str__(self):
        return self.FractionStr()

    def __float__(self):
        return self.value

    def __round__(self, n=0):
        return self

    def Reciprocal(self, __atype__="instanceobj, returns a fraction"):
        return Fraction("{0:d}/{1:d}".format(self.denominator, self.numerator))

    def Simplify(self, __atype__="instanceobj, returns nothing but simplifies fraction in place"):
        gcd = Fraction.GCD(abs(self.numerator), self.denominator)
        self.numerator //= gcd
        self.denominator //= gcd

    def PrettyPrint(self):
        print(self.numerator, end='')
        if self.numerator == 0 or self.denominator == 1:
            print()
        else:
            print("/", end='')
            print(self.denominator)

    def FractionStr(self):
        s = "{0:d}".format(int(self.numerator))
        if self.numerator != 0 and self.denominator != 1:
            s += "/"
            s += "{0:d}".format(int(self.denominator))

        return s

    def ContinuedFraction(self, __atype__="instanceobj, prints current fraction as a continued fraction and returns"):
        continuedFraction = [self.numerator//self.denominator]
        Fraction.EuclidContinuedFraction(self.numerator, self.denominator, continuedFraction)
        Fraction.PrettyPrintContinuedFraction(continuedFraction, self.numerator//abs(self.numerator))
        return Pause()

    @classmethod
    def LCM(cls, n1, n2, __atype__="classobj, int, int, returns an integer"):
        return Fraction.EuclidLCM(n1, n2)

    @classmethod
    def GCD(cls, n1, n2, __atype__="classobj, int, int, returns an integer"):
        return Fraction.EuclidGCD(n1, n2)

    @classmethod
    def PrimeFactors(cls, num, __atype__="classobj, int, returns a list of integers"):
        if num <= 0:
            raise Exception("Only numbers greater than 0 please")

        factors = []

        while num % 2 == 0:
            factors.append(2)
            num //= 2

        for i in range(3, int(math.sqrt(num))+1, 2):
            while num % i == 0:
                factors.append(i)
                num //= i

        if num != 1: factors.append(num)

        return factors

    @classmethod
    def PrimeFactorsLCM(cls, n1, n2, __atype__="classobj, int, int, returns an integer"):
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
    def PrimeFactorsGCD(cls, n1, n2, __atype__="classobj, int, int, returns an integer"):
        factors1 = Fraction.PrimeFactors(n1)
        factors2 = Fraction.PrimeFactors(n2)

        commonFactor = 1
        for f in factors1:
            if f in factors2:
                commonFactor *= f
                factors2.remove(f)

        return commonFactor

    @classmethod
    def EuclidLCM(cls, n1, n2, __atype__="classobj, int, int, returns an integer"):
        return (n1 * n2)//Fraction.EuclidGCD(n1, n2)

    @classmethod
    def EuclidGCD(cls, n1, n2, __atype__="classobj, int, int, returns an integer"):
        if (max(n1, n2) % min(n1, n2) == 0):
            return min(n1, n2)

        return Fraction.EuclidGCD(min(n1, n2), max(n1, n2) % min(n1, n2))

    @classmethod
    def EuclidContinuedFraction(cls, n1, n2, cF):
        if (max(n1, n2) % min(n1, n2) == 0):
            cF.append(n1//n2)
            return

        cF.append(max(n1, n2)//min(n1, n2))
        Fraction.EuclidContinuedFraction(min(n1, n2), max(n1, n2) % min(n1, n2), cF)

    @classmethod
    def FromDecimal(cls, decimal, __atype__="classobj, float, returns a fraction"):
        continuedFraction, sign = Fraction.GenerateContinuedFraction(decimal)
        return Fraction.RollupContinuedFraction(continuedFraction, sign)

    # Rollup the continued fraction
    @classmethod
    def RollupContinuedFraction(cls, continuedFraction, sign=1, __atype__="classobj, list:int, returns a fraction"):
        pf = Fraction('0/1')
        for i in range(len(continuedFraction), 0, -1):
            if i == 1:
                return (pf + continuedFraction[i-1]) * sign

            if i == len(continuedFraction):
                pf = Fraction("1/{0:d}".format(continuedFraction[i-1]))

            else:
                pf = Fraction('1/1') / (pf + continuedFraction[i-1])

    # Generate a continued fraction from a decimal
    @classmethod
    def GenerateContinuedFraction(cls, decimal, __atype__="classobj, float, returns a list of integers and the sign of that list"):
        continuedFraction = []
        d, sign = (math.fabs(decimal), int(not decimal or decimal/math.fabs(decimal)))
        whole, remaining = (int(d), float("0.{0:s}".format(str(d)[(len(str(int(d)))+1):])))
        continuedFraction.append(whole)

        loop = 0
        while remaining > 0.00001 and loop < 16:
            reciprocal = 1/remaining
            whole, remaining = (int(reciprocal), float("0.{0:s}".format(str(reciprocal)[(len(str(int(reciprocal)))+1):])))
            continuedFraction.append(whole)
            loop += 1

        return continuedFraction, sign

    @classmethod
    def PrintContinuedFraction(cls, decimal, __atype__="classobj, float, prints decimal as a continued fraction and returns"):
        continuedFraction, sign = Fraction.GenerateContinuedFraction(decimal)
        Fraction.PrettyPrintContinuedFraction(continuedFraction, sign)
        return Pause()

    @classmethod
    def PrettyPrintContinuedFraction(cls, continuedFraction, sign):
        # Set the count for number of spaces
        count = 0
        # Print "-1 * (" if it is a negative number
        if sign < 0:
            print("-1 * (", end='')
            count += 6

        if continuedFraction[len(continuedFraction)-1] == 1:
            continuedFraction[len(continuedFraction)-2] += 1
            continuedFraction.pop(len(continuedFraction)-1)

        for i in range(0, len(continuedFraction)):
            # Print the next number of the continued Fraction
            print(continuedFraction[i], end='')

            # If last number, print a new line and we are done
            if i+1 == len(continuedFraction):
                if sign < 0: print(")")  # if a negative number print closing ")" before new line
                print('')
                return

            # Print "+ 1" and a new line
            print(" + ", end='')
            print(1)

            # Increment count by the length of the continued fraction and 4 more for the + 1
            count += len(str(continuedFraction[i]))+3

            # Create a space string of length count and print
            s = ""
            for j in range(0, count): 
                s += " "
            print(s, end='')

            # Calculate length of the fraction line it is length of next number plus 4 (for " + 1"), unless last but one
            if i+2 == len(continuedFraction):
                countL = len(str(continuedFraction[i+1]))
            else:
                countL = len(str(continuedFraction[i+1]))+4

            # Generate the fraction line and print with a new line
            l = ""
            for j in range(0, countL):
                l += "-"
            print(l)

            # Then print as many spaces as needed and loop back to next number
            print(s, end='')
