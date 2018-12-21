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

    def __init__(self, eString):
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

            equation = OrderedDict(sorted(equation.items(), key=lambda t: t[0]))
            equations.append(equation)

        variables = []
        varStr = ""
        rhsStr = ""
        for equation in equations:
            for var in equation.keys():
                if var not in variables and var is not 'rhs':
                    variables.append(var)
                    varStr += "%s:" % var

                if var is 'rhs':
                    rhsStr += "%.2f:" % float(equation['rhs'])

        coeffStr = ""
        for equation in equations:
            for i in range(0, len(variables)):
                var = variables[i]
                if var in equation.keys():
                    coeffStr += "%.2f" % float(equation[var])
                else:
                    coeffStr += "%.2f" % float(0)
                if i != len(variables)-1:
                    coeffStr += ","

            coeffStr += ":"

        self.A = Matrix(coeffStr)
        self.X = Matrix(varStr)
        self.B = Matrix(rhsStr)
        self.isValid = True
        self.nVariables = len(variables)

        if self.nVariables != self.nEquations:
            raise Exception("Numbers of variables (%d) and number of equations don't match (%d)" % (self.nVariables, self.nEquations))


    def PrettyPrintSystemOfEquations(self):
        a = Matrix.CreateBlank(self.nEquations, self.nVariables)
        for i in range (0, a.rSize):
            for j in range(0, a.cSize):
                ix = i * a.cSize + j
                if type(self.A.elements[ix]) is str:
                    a.elements[ix] = self.A.elements[ix]
                else:
                    a.elements[ix] = "%.2f" % self.A.elements[ix]
                if a.elements[ix] == '-0.00':
                    a.elements[ix] = '0.00'

        x = Matrix.CreateBlank(self.nVariables, 1)
        for i in range (0, x.rSize):
            for j in range(0, x.cSize):
                ix = i * x.cSize + j
                if type(self.X.elements[ix]) is str:
                    x.elements[ix] = self.X.elements[ix]
                else:
                    x.elements[ix] = "%.2f" % self.X.elements[ix]
                if x.elements[ix] == '-0.00':
                    x.elements[ix] = '0.00'

        b = Matrix.CreateBlank(self.nEquations, 1)
        for i in range (0, b.rSize):
            for j in range(0, b.cSize):
                ix = i * b.cSize + j
                if type(self.B.elements[ix]) is str:
                    b.elements[ix] = self.B.elements[ix]
                else:
                    b.elements[ix] = "%.2f" % self.B.elements[ix]
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

