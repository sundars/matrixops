from overrides import *
import math
from matrix import Matrix
from collections import OrderedDict

class LinearEquations():
    A = None
    B = None
    X = None
    nEquations = 0
    nVariables = 0
    isValid = False
    keepFraction = False

    def __init__(self, eString, keepFraction=False):
        if eString == "":
            return

        # array if equation dictionary
        equations = []

        # split equation string in the the different equations
        eqns = eString.split(':')
        self.nEquations = len(eqns)
        if self.nEquations == 0 or (self.nEquations == 1 and eqns[0] == ""):
            raise Exception("No equations in input\nFormat for equations is: 2*a+3*b+1*c=4:5*a-1*c=1:...")

        # ignore the last ':'
        if eqns[self.nEquations-1] == "":
            eqns.pop()
            self.nEquations -= 1

        # for each equation
        for eqn in eqns:
            # single equation dictionary
            equation = OrderedDict()

            # split the equation into the lhs and rhs
            parts = eqn.split('=')
            assert (len(parts) == 2), "Malformed equation %s" % eqn
            lhs = parts[0]
            rhs = parts[1]

            # parse a single equation string
            c = 0
            np = lhs.find('+', c+1)
            nm = lhs.find('-', c+1)
            while not (nm == -1 and np == -1 and c == len(lhs)):
                n = min(nm, np)
                if n == -1: n = max(nm, np)
                if n == -1: n = len(lhs)

                s = lhs[c:n]
                coeff = s.split("*")
                assert (len(coeff) == 2), "Malformed coefficient %s" % s
                equation[coeff[1]] = coeff[0]

                c = n
                np = lhs.find('+', c+1)
                nm = lhs.find('-', c+1)

            equation['rhs'] = rhs
            equations.append(equation)

        variables = []
        for equation in equations:
            for var in equation.keys():
                if var not in variables and var is not 'rhs':
                    variables.append(var)

        variables.sort()
        varStr = ""
        for var in variables:
            varStr += "%s:" % var

        coeffStr = ""
        rhsStr = ""
        for equation in equations:
            for i in range(0, len(variables)):
                var = variables[i]
                if var in equation.keys():
                    coeffStr += str(float(equation[var]))
                else:
                    coeffStr += str(float(0))
                if i != len(variables)-1:
                    coeffStr += ","

            rhsStr += str(float(equation['rhs']))
            coeffStr += ":"

        self.A = Matrix(coeffStr, keepFraction)
        self.X = Matrix(varStr, False)
        self.B = Matrix(rhsStr, keepFraction)
        self.isValid = True
        self.nVariables = len(variables)
        self.keepFraction = keepFraction

        if self.nVariables != self.nEquations:
            raise Exception("Numbers of variables (%d) and number of equations don't match (%d)" % (self.nVariables, self.nEquations))

    def CheckSolution(self, soln):
        if soln.rSize != self.nVariables and soln.cSize != 1:
            raise Exception("Solution matrix should be a %dx1 matrix" % self.nVariables)

        return self.A.Multiply(soln).IsEqual(self.B)

    def PrettyPrintSystemOfEquations(self):
        a = Matrix.CreateBlank(self.nEquations, self.nVariables)
        for i in range (0, a.rSize):
            for j in range(0, a.cSize):
                ix = i * a.cSize + j
                a.elements[ix] = str(self.A.elements[ix])

                if a.elements[ix] == '-0.00':
                    a.elements[ix] = '0.00'

        x = Matrix.CreateBlank(self.nVariables, 1)
        for i in range (0, x.rSize):
            for j in range(0, x.cSize):
                ix = i * x.cSize + j
                x.elements[ix] = str(self.X.elements[ix])

                if x.elements[ix] == '-0.00':
                    x.elements[ix] = '0.00'

        b = Matrix.CreateBlank(self.nEquations, 1)
        for i in range (0, b.rSize):
            for j in range(0, b.cSize):
                ix = i * b.cSize + j
                b.elements[ix] = str(self.B.elements[ix])

                if b.elements[ix] == '-0.00':
                    b.elements[ix] = '0.00'

        just1 = a.GetLargestSize() + 1
        just2 = x.GetLargestSize() + 1
        just3 = b.GetLargestSize() + 1
        for i in range(0, max(a.rSize, x.rSize, b.rSize)):
            if i < a.rSize:
                print "|",
            else:
                print " ",
            for j in range(0, a.cSize):
                ix = i * a.cSize + j
                if i < a.rSize:
                    print a.elements[ix].rjust(just1),
                else:
                    print ''.rjust(just1),
            if i < a.rSize:
                print "|",
            else:
                print " ",

            if i == round(a.rSize/2):
                print " * ",
            else:
                print "   ",

            if i < x.rSize:
                print "|",
            else:
                print " ",
            for j in range(0, x.cSize):
                ix = i * x.cSize + j
                if i < x.rSize:
                    print x.elements[ix].rjust(just2),
                else:
                    print ''.rjust(just2),
            if i < x.rSize:
                print "|",
            else:
                print " ",

            if i == round(a.rSize/2):
                print " = ",
            else:
                print "   ",

            if i < b.rSize:
                print "|",
            else:
                print " ",
            for j in range(0, b.cSize):
                ix = i * b.cSize + j
                if i < b.rSize:
                    print b.elements[ix].rjust(just3),
                else:
                    print ''.rjust(just3),
            if i < b.rSize:
                print "|",
            else:
                print " ",
            print

