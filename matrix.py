import math

class Matrix():
    elements = []
    rSize = 0
    cSize = 0
    isValid = False

    def __init__(self, s):
        self.elements = []
        self.rSize = 0
        self.cSize = 0
        self.isValid = False

        if s is not "":
            rows = s.split(':')
            if len(rows) == 1:
                # Assume square matrix
                for element in s.split(','):
                    try:
                        self.elements.append(float(element))
                    except Exception, e:
                        self.elements.append(element)

                self.rSize = self.cSize = int(math.sqrt(len(self.elements)))
                if self.rSize ** 2 != len(self.elements):
                    raise Exception("Expected square matrix\nElse specify as a11,a12,...a1n:a21,a22,...a2n:...:am1,am2...amn:")

            else:
                self.rSize = len(rows)
                if rows[self.rSize-1] == "":
                    self.rSize -= 1
                for i in range(0, self.rSize):
                    for element in rows[i].split(','):
                        try:
                            self.elements.append(float(element))
                        except Exception, e:
                            self.elements.append(element)

                self.cSize = int(len(self.elements)/self.rSize)
                if self.rSize*self.cSize != len(self.elements):
                    raise Exception("Matrix isn't properly formatted\nFormat as a11,a12,...,a1n:a21,a22,...,a2n:...:am1,am2,...,amn:")

            self.isValid = True

    # Return the element in rth row cth column
    def GetElement(self, r, c):
        return self.elements[r * self.cSize + c]

    # Set the element in rth row cth column to val
    def SetElement(self, r, c, val):
        self.elements[r * self.cSize + c] = val

    def MakeCopy(self):
        m = Matrix.CreateBlank(self.rSize, self.cSize)
        for i in range(0, m.rSize * m.cSize):
            m.elements[i] = self.elements[i]

        return m

    # Return True if and only if it is a square matrix
    def IsSquare(self):
        return self.rSize == self.cSize

    # Return True if and only m can be left multiplied by self
    def CanMultiply(self, m):
        return self.cSize == m.rSize

    # Matrix multiplication - m left multiplied by self
    # Output is the product of the two matrices
    def Multiply(self, m):
        if not self.CanMultiply(m):
            raise Exception("Cannot multiply these two matrices")

        p = Matrix.CreateBlank(self.rSize, m.cSize)
        x = 0
        for i in range(0, self.rSize):
            for j in range(0, m.cSize):
                element = 0
                for k in range(0, self.cSize):
                    selfIndex = i * self.cSize + k
                    mIndex = k * m.cSize + j
                    element += self.elements[selfIndex] * m.elements[mIndex]

                x = i * m.cSize + j
                p.elements[x] = element

        return p

    # Find determinant - a recursive function
    def Determinant(self):
        if not self.IsSquare():
            raise Exception("Cannot calculate determinant of non-square matrix")

        if self.rSize == 1:
            return self.elements[0]

        value = 0
        sign = 1
        for i in range(0, self.rSize):
            value += sign * self.elements[i] * self.GetSubmatrix(0, i).Determinant()
            sign *= -1

        return value

    # Return matrix of minors - only for a square matrix
    def MatrixOfMinors(self):
        if not self.IsSquare():
            raise Exception("Cannot calculate matrix of minors of non-square matrix")

        minors = Matrix.CreateBlank(self.rSize, self.cSize)
        for i in range(0, self.rSize):
            for j in range(0, self.cSize):
                minor = self.GetSubmatrix(i, j).Determinant()
                x = i * self.cSize + j
                minors.elements[x] = minor

        return minors

    # Return matrix of cofactors - only for a square matrix
    def MatrixOfCofactors(self):
        if not self.IsSquare():
            raise Exception("Cannot calculate matrix of cofactors of non-square matrix")

        cofactors = Matrix.CreateBlank(self.rSize, self.cSize)
        sign1 = sign2 = 1
        for i in range(0, self.rSize):
            for j in range(0, self.cSize):
                x = i * self.cSize + j
                cofactors.elements[x] = sign1 * sign2 * self.elements[x]
                sign2 *= -1
            sign2 = 1
            sign1 *= -1

        return cofactors

    # Row Reduction operation - done in place within the matrix
    # Inputs:
    #        1. Row 1 (r1) to be manipulated
    #        2. Row 2 (r2) using row2 during manipulation, if none this is passed as -1, always r1 - r2
    #        3. Multiplier (m1) to apply to row 1, if 1 simple subtraction, if -1 simple addition
    #        4. Multiplier (m2) to apply to row 2, if 1 simple subtraction, if -1 simple addition
    def RowReduce(self, r1, r2, m1, m2):
        for i in range(0, self.cSize):
            x1 = r1 * self.cSize + i
            if r2 == -1:
                self.elements[x1] *= m1
            else:
                x2 = r2 * self.cSize + i
                self.elements[x1] = self.elements[x1] * m1 - self.elements[x2] * m2

    # Transpose of a matrix
    def Transpose(self):
        t = Matrix.CreateBlank(self.cSize, self.rSize)

        for i in range(0, self.rSize):
            for j in range(0, self.cSize):
                x = i * self.cSize + j
                tx = j * self.rSize + i
                t.elements[tx] = self.elements[x]

        return t

    # Return Inverse of Matrix - must be square
    def Inverse(self):
        if not self.IsSquare():
            raise Exception("Cannot calculate inverse of non-square matrix")

        det = self.Determinant()
        if det == 0:
            raise Exception("Inverse doesn't exist for matrix")

        inv = self.MatrixOfMinors().MatrixOfCofactors().Transpose()
        inv.ScalarMultiply(1/det)
        return inv

    # Any 2 matrices
    def IsEqual(self, m):
        if len(self.elements) != len(m.elements):
            return False

        if self.rSize != m.rSize:
            return False

        for i in range(0, len(self.elements)):
            if math.fabs(self.elements[i] - m.elements[i]) > 0.001:
                return False

        return True

    # Remove row and column from this matrix and return remaining matrix
    def GetSubmatrix(self, row, column):
        s = Matrix.CreateBlank(self.rSize-1, self.cSize-1)
        sx = 0;
        for i in range(0, self.rSize):
            for j in range(0, self.cSize):
                x = i * self.cSize + j
                if i != row and j != column:
                    s.elements[sx] = self.elements[x]
                    sx += 1

        return s

    # Multiply matrix with a scalar
    def ScalarMultiply(self, val):
        for i in range(0, self.rSize):
            for j in range(0, self.cSize):
                x = i * self.cSize + j
                self.elements[x] *= val

    # Returns true if it is an identity (and therefore square) matrix
    def IsIdentityMatrix(self):
        if not self.IsSquare():
            return False

        for i in range(0, self.rSize):
            for j in range(0, self.cSize):
                x = i * self.cSize + j
                if i == j:
                    if self.elements[x]-1.0 > 0.001: return False
                else:
                    if self.elements[x]-0.0 > 0.001: return False

        return True

    # Get the size of the largest element in matrix - for pretty printing purposes
    def GetLargestSize(self):
        l = 2
        for i in range(0, self.rSize):
            for j in range(0, self.cSize):
                x = i * self.cSize + j
                if len(str(self.elements[x])) > l:
                    l = len(str(self.elements[x]))

        return l

    # Pretty print a matrix, aligning rows and columns
    def PrettyPrintMatrix(self):
        m = Matrix.CreateBlank(self.rSize, self.cSize)
        for i in range(0, self.rSize):
            for j in range(0, self.cSize):
                x = i * self.cSize + j
                if type(self.elements[x]) is str:
                    m.elements[x] = self.elements[x]
                else:
                    m.elements[x] = "%.2f" % self.elements[x]
                if m.elements[x] == '-0.00':
                    m.elements[x] = '0.00'

        just = m.GetLargestSize() + 1
        for i in range(0, m.rSize):
            for j in range(0, m.cSize):
                x = i * m.cSize + j
                print m.elements[x].rjust(just),
            print

    # Pretty print two  matrices side by side
    @classmethod
    def PrettyPrintTwoMatrices(cls, matrix1, matrix2):
        m1 = Matrix.CreateBlank(matrix1.rSize, matrix1.cSize)
        for i in range (0, matrix1.rSize):
            for j in range(0, matrix1.cSize):
                x = i * matrix1.cSize + j
                if type(matrix1.elements[x]) is str:
                    m1.elements[x] = matrix1.elements[x]
                else:
                    m1.elements[x] = "%.2f" % matrix1.elements[x]
                if m1.elements[x] == '-0.00':
                    m1.elements[x] = '0.00'

        m2 = Matrix.CreateBlank(matrix2.rSize, matrix2.cSize)
        for i in range (0, matrix2.rSize):
            for j in range(0, matrix2.cSize):
                x = i * matrix2.cSize + j
                if type(matrix2.elements[x]) is str:
                    m2.elements[x] = matrix2.elements[x]
                else:
                    m2.elements[x] = "%.2f" % matrix2.elements[x]
                if m2.elements[x] == '-0.00':
                    m2.elements[x] = '0.00'

        just1 = m1.GetLargestSize() + 1
        just2 = m2.GetLargestSize() + 1
        for i in range(0, max(matrix1.rSize, matrix2.rSize)):
            for j in range(0, m1.cSize):
                x = i * m1.cSize + j
                if i < m1.rSize:
                    print m1.elements[x].rjust(just1),
                else:
                    print ''.rjust(just1),

            print "      ",
            for j in range(0, m2.cSize):
                x = i * m2.cSize + j
                if i < m2.rSize:
                    print m2.elements[x].rjust(just2),
                else:
                    print ''.rjust(just2),
            print

    # Returns a square matrix
    @classmethod
    def GetIdentityMatrix(cls, size):
        m = Matrix.CreateBlank(size, size)

        for i in range(0, size):
            for j in range (0, size):
                x = i * size + j
                if (i == j):
                    m.elements[x] = 1.0
                else:
                    m.elements[x] = 0.0

        return m

    # Get row row from self and column column from m
    @classmethod
    def GetRowColumn(cls, m1, m2, row, column):
        r = []
        c = []
        for i in range(0, m1.cSize):
            x = row * m1.cSize + i
            r.append(m1.elements[x])

        for i in range(0, m2.rSize):
            x = column + i * m2.cSize
            c.append(m2.elements[x])

        return (r, c)

    # Creates a blank rxc matrix with '...' as placeholders
    @classmethod
    def CreateBlank(cls, rSize, cSize):
        if rSize == 0 or cSize == 0:
            return None

        b = ""
        for i in range(0, rSize):
            for j in range(0, cSize):
                b += "..."
                if j == cSize-1:
                    b += ':'
                else:
                    b += ','

        return Matrix(b)
