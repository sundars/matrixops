import sys, getopt, math
from matrix import Matrix
from equation import LinearEquations

step = 0
showHint = False

def main():
    calculateInverse, calculateDeterminant, m1, m2, soe = parseArgs()

    print
    if m2 is not None:
        print "Input matrices are:"
        Matrix.PrettyPrintTwoMatrices(m1, m2)
        print
        if calculateDeterminant: print "- Calculate determinant of first matrix"
        if calculateInverse: print "- Calculate inverse of first matrix"
        print "- Left multiply second matrix with the first matrix"
    else:
        if m1 is not None:
            print "Input matrix is:"
            m1.PrettyPrintMatrix()
            print
            if calculateDeterminant: print "- Calculate determinant of this matrix"
            if calculateInverse: print "- Calculate inverse of this matrix"

    if soe is not None:
        print
        print "System of Equations is:"
        soe.PrettyPrintSystemOfEquations()
        print
        print "- Find solution to this system of equations"

    print_space()

    if (not calculateInverse and not calculateDeterminant and m2 is None and soe is None):
        print "No operation specified, nothing do... have a nice day"
        sys.exit(0)

    if calculateDeterminant:
        try:
            det = m1.Determinant()
            print "Determinant = ", det
            print_space()

        except Exception, e:
            print(e)
            print_space()

    if calculateInverse:
        try:
            inverseMatrix = m1.Inverse()

            inv = step_by_step_inverse_cofactors(m1)
            if not inverseMatrix.IsEqual(inv):
                raise Exception("Oops! got the wrong inverse using cofactors method")

            inv = step_by_step_guass_jordan(m1)
            if inverseMatrix.IsEqual(inv):
                print "Yay! got the correct inverse using Guass Jordan method"
            else:
                inv.PrettyPrintMatrix()
                raise Exception("Oops! got the wrong inverse using Guass Jordan method")

            print "The inverse matrix is:"
            inverseMatrix.PrettyPrintMatrix()
            print_space()

            # Check if inverse is correct
            print "Multiplying a matrix and its inverse will give..."
            Matrix.PrettyPrintTwoMatrices(m1, inverseMatrix)
            print_raw_input("Press Enter to continue...")
            productMatrix = m1.Multiply(inverseMatrix)
            if not productMatrix.IsIdentityMatrix():
                print "Something went wrong..."
                productMatrix.PrettyPrintMatrix()
                print_space()
            print "The identity matrix:"
            productMatrix.PrettyPrintMatrix()
            print_space()

        except Exception, e:
            print(e)
            print_space()

    if m2 is not None:
        try:
            productMatrix = m1.Multiply(m2)

            print "Multiply the following two matrices:"
            Matrix.PrettyPrintTwoMatrices(m1, m2)
            print_raw_input("Press Enter to continue...")

            productMatrix = step_by_step_multiply(m1, m2)
            print "Product matrix:"
            productMatrix.PrettyPrintMatrix()
            print_space()

        except Exception, e:
            print(e)
            print_space()

    if soe is not None:
        try:
            solutionMatrix = step_by_step_guass_jordan(soe.A, soe.B)

            if soe.CheckSolution(solutionMatrix):
                print("Yay! got the correct solution to the system of equations")
            else:
                raise Exception("Oops! got the wrong solution")

            print "The solution to the system of equations is:"
            Matrix.PrettyPrintTwoMatrices(soe.X, solutionMatrix)
            print_space()

        except Exception, e:
            print(e)
            print_space()

    sys.exit(0)

# Exercise: Remove the code for this function and the ones for both row reduction functions below for students to implement
# This function should return
#    1. The inverse of m1 if m2 is None or
#    2. Row reduced m2 (used for systems of equations)
#
# Inputs are
#    m1: matrix to be row reduced to identity
#    m2: perform same operations on m2, if None perform same operations on identity
def step_by_step_guass_jordan(m1, m2=None):
    global step
    # Make a copy - python is effectively pass by reference
    matrix = m1.MakeCopy()
    if m2 is None:
        inverseMatrix = Matrix.GetIdentityMatrix(matrix.rSize)
    else:
        inverseMatrix = m2.MakeCopy()

    if inverseMatrix.IsSquare():
        print "Use Guass Jordan elimination and row-echelon form to find inverse of:"
    else:
        print "Use Guass Jordan elimination to find the solution to the system of linear equations:"
    Matrix.PrettyPrintTwoMatrices(matrix, inverseMatrix)
    print_raw_input("Press Enter to continue...")

    # Row reduce down to get to row-echelon form
    step = 0
    for i in range(0, matrix.rSize):
        if not matrix.IsIdentityMatrix():
            matrix, inverseMatrix = row_reduce_down(matrix, inverseMatrix, i)
        else:
            return inverseMatrix

    # Row reduce up to get inverse, last row already in proper form
    for i in range(matrix.rSize-1, 0, -1):
        if not matrix.IsIdentityMatrix():
            matrix, inverseMatrix = row_reduce_up(matrix, inverseMatrix, i-1)
        else:
            return inverseMatrix

    return inverseMatrix

# Row reduction down - for Guass Jordan method. At the end of this matrix will be in row-echelon form
def row_reduce_down(m, inv, row):
    global step

    # If the diagonal element is 0, need to add row with another whose corresponding column is non-zero
    # one such row is guaranteed to exist, otherwise determinant will be 0
    if m.IsValue(row, row, 0):
        add_row_to_make_diagonal_nonzero(m, inv, row)

    # Make all elements before the diagonal 0 by subtracting from rows above
    if row > 0:
        step += 1
        hint = 0
        show_hint("Step %d: Make all elements in row %d, before column %d equal 0. Next..." % (step, row+1, row+1))
        for i in range(0, row):
            element = m.GetElement(row, i)
            if not m.IsValue(row, i, 0):
                if element != 1:
                    m.RowReduce(row, -1, 1/element, 1)
                    inv.RowReduce(row, -1, 1/element, 1)
                    hint += 1
                    show_hint("    Hint %d.%d: Divide row %d by %.2f. Next..." % (step, hint, row+1, element), True, m, inv)

                m.RowReduce(row, i, 1, 1)
                inv.RowReduce(row, i, 1, 1)
                hint += 1
                show_hint("    Hint %d.%d: Subtract row %d from row %d. Next..." % (step, hint, i+1, row+1), True, m, inv)

        if showHint and hint == 0:
            print_raw_input("    Already 0, nothing to do...") 

    # Make the diagonal element 1
    diagElement = m.GetElement(row, row)
    if not m.IsValue(row, row, 1):
        step += 1
        hint = 0
        show_hint("Step %d: Make the element in row %d, column %d equal 1. Next..." % (step, row+1, row+1))

        m.RowReduce(row, -1, 1/diagElement, 1)
        inv.RowReduce(row, -1, 1/diagElement, 1)
        hint += 1
        show_hint("    Hint %d.%d: Divide row %d by %.2f. Next..." % (step, hint, row+1, diagElement), True, m, inv)

    return m, inv

# Row reduction up - for Guass Jordan method - at the end of this we will have inverse
def row_reduce_up(m, inv, row):
    global step

    # Make all elements after the diagonal 0 by subtracting from rows below
    step += 1
    hint = 0
    show_hint("Step %d: Make all elements in row %d, after column %d equal 0. Next..." % (step, row+1, row+1))
    for i in range(m.rSize-1, row, -1):
        element = m.GetElement(row, i)

        if not m.IsValue(row, i, 0):
            m.RowReduce(row, i, 1, element)
            inv.RowReduce(row, i, 1, element)
            if element != 1:
                hint += 1
                show_hint("    Hint %d.%d: Multiply row %d by: %.2f and subtract from row %d. Next..."
                               % (step, hint, i+1, element, row+1), True, m, inv)
            else:
                hint += 1
                show_hint("    Hint %d.%d: Subtract row %d from row %d. Next..." % (step, hint, i+1, row+1), True, m, inv)

    if showHint and hint == 0:
        print_raw_input("   Already 0, nothing to do...") 

    return m, inv

# Row reduce to make diagnoal non-zero (may need to add 2 rows in some instances
def add_row_to_make_diagonal_nonzero(m, inv, row):
    global step
    step += 1
    hint = 0
    show_hint("Step %d: Make the element in row %d, column %d non-zero. Next..." % (step, row+1, row+1))
    for i in range(1, m.rSize):
        ar = (row + i) % m.rSize

        if not m.IsValue(ar, row, 0) and (not m.IsValue(row, ar, 0) or not m.IsValue(ar, ar, 1)):
            m.RowReduce(row, ar, 1, -1)
            inv.RowReduce(row, ar, 1, -1)
            hint += 1
            show_hint("    Hint %d.%d: Add row %d to row %d. Next..." % (step, hint, ar+1, row+1), True, m, inv)
            return

    # still zero
    if m.IsValue(row, row, 0):
        # Need to add 2 rows together
        for i in range(1, m.rSize):
            ar1 = (row + i) % m.rSize

            if not m.IsValue(ar1, row, 0):
                for j in range(i+1, m.rSize+i):
                    ar2 = (row + j) % m.rSize

                    if not m.IsValue(ar2, ar1, 0):
                        # Add first row found
                        m.RowReduce(row, ar1, 1, -1)
                        inv.RowReduce(row, ar1, 1, -1)

                        # Add second row found
                        m.RowReduce(row, ar2, 1, -1)
                        inv.RowReduce(row, ar2, 1, -1)
                        hint += 1
                        show_hint("    Hint %d.%d: Add rows %d and %d to row %d. Next..."
                                   % (step, hint, ar1+1, ar2+1, row+1), True, m, inv)
                        return

# Inverse via minors, cofactors and adjugate - to double check Guass Jordan elimination
def step_by_step_inverse_cofactors(m):
    show_hint("Calculate inverse using matrix of minors, cofactors and adjugate\n")

    minors = m.MatrixOfMinors()
    show_hint("Step 1: Find determinant of sub-matrices to get Matrix of Minors. Next...", True, minors)

    cofactors = minors.MatrixOfCofactors()
    show_hint("Step 2: Alternate +/- on minors matrix to get Matrix of Cofactors. Next...", True, cofactors)

    adjugate = cofactors.Transpose()
    show_hint("Step 3: Transpose the cofactors matrix to get Adjugate Matrix. Next...", True, adjugate)

    det = m.Determinant()
    adjugate.ScalarMultiply(1/det)
    inv = adjugate.MakeCopy()
    show_hint("Step 4: Divide adjugate by determinant to get inverse Matrix. Next...", True, inv)

    if showHint:
        print "Inverse matrix is:"
        inv.PrettyPrintMatrix()
        print_space()

    return inv

# step by step multiplication of two matrices
def step_by_step_multiply(m1, m2):
    global step
    matrix = Matrix.CreateBlank(m1.rSize, m2.cSize)

    step = 0
    for i in range(0, m1.rSize):
        for j in range(0, m2.cSize):
            step += 1
            show_hint("Step %d: Multiply corresponding elements in row %d of 1st matrix and column %d of 2nd matrix and add up..."
                      % (step, i+1, j+1))

            row, column = Matrix.GetRowColumn(m1, m2, i, j)
            s = ""
            element = 0
            for k in range(0, m1.cSize):
                element += row[k] * column[k]
                if k == m1.cSize - 1:
                    s += "%.2f * %.2f = %.2f\n" % (row[k], column[k], element)
                else:
                    s += "%.2f * %.2f + " % (row[k], column[k])
            matrix.SetElement(i, j, element)
            show_hint(s, True, matrix, None)

    return matrix


# Utility that prints out hints
def show_hint(s, prettyPrint=False, m1=None, m2=None):
    global showHint
    if not showHint: return
    raw_input(s)
    if prettyPrint:
        if m2 is not None:
            Matrix.PrettyPrintTwoMatrices(m1, m2)
        else:
            m1.PrettyPrintMatrix()

        print_raw_input("Press Enter to continue...")

def print_space():
    print
    print "------------------------------------------------------------------------------------"
    print

def print_raw_input(s):
    raw_input(s)
    print

def parseArgs():
    global showHint
    sarg = ""
    marg = ""
    parg = ""
    calculateInverse = False
    calculateDeterminant = False

    # Get the inputs/arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vhids:p:m:', ['matrix=', 'matrix-multiply=' 'system-of-equations='])
    except getopt.GetoptError:
        usage()

    # Parse the arguments
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-i', '--inverse'):
            calculateInverse = True
        elif opt in ('-d', '--determinant'):
            calculateDeterminant = True
        elif opt in ('-v', '--verbose-hints'):
            showHint = True
        elif opt in ('-m', '--matrix'):
            marg = arg
        elif opt in ('-p', '--matrix-multiply'):
            parg = arg
        elif opt in ('-s', '--system-of-equations'):
            sarg = arg
        else:
            usage()

    try:
        s = LinearEquations(sarg)

        # Parse the matrices
        m1 = Matrix(marg)
        if (not m1.isValid and not s.isValid):
            raise Exception("either -m MATRIX or -s EQNS is a required argument")

        m2 = Matrix(parg)

        if (not s.isValid): s = None
        if (not m1.isValid): m1 = None
        if (not m2.isValid): m2 = None

        if (calculateInverse or calculateDeterminant) and (not m1.IsSquare()):
            raise Exception("Must specify square matrix to calculate inverse or determinant")

        return (calculateInverse, calculateDeterminant, m1, m2, s)
    except Exception, e:
        print(e)
        usage()

# Usage for this program
def usage():
    print
    print sys.argv[0] + " [options]"
    print "Matrix is required:"
    print " -m MATRIX, --matrix=MATRIX          Square matrix formatted as a11,a12,...,a1n,a21,a22,...,a2n,...,an1,an2,...,ann"
    print "                                     Non-square formatted as a11,a12,...,a1n:a21,a22,...,a2n:...:am1,am2,...,amn:"
    print " -s EQNS --system-of-equations=EQNS  specify a system of equations to solve"
    print "                                     Format is: 2*a+3*b+1*c=4:5*a-1*c=1:..."
    print "Options:"
    print " -p MATRIX --matrix-multiply=MATRIX  left multiply matrix provided by -m with the one provided by -p"
    print " -i --inverse                        calculate the inverse of matrix"
    print " -d --determinant                    calculate the determinant of matrix"
    print " -v --verbose-hint                   show verbose hints for Guass Jordan elimination method"
    print " -h, --help                          show this help message and exit"
    sys.exit(1)

main()
