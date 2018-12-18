import getopt, sys, math

step = 0
showHint = False

def main():
    matrix = []
    calculateInverse, calculateDeterminant, elements = parseArgs()
    for e in elements.split(','):
        matrix.append(float(e))

    matrixSize = int(math.sqrt(len(matrix)))
    if matrixSize ** 2 != len(matrix):
        print "Matrix must be a square matrix"
        usage()
        sys.exit(3)

    print
    print "Input matrix is:"
    pretty_print_matrix(matrix, matrixSize)
    print
    print "------------------------------------------------------------------------------------"
    print

    if calculateDeterminant:
        det = determinant(matrix, matrixSize)
        print "Determinant = ", det;
        print
        print "------------------------------------------------------------------------------------"
        print

    if calculateInverse:
        inverseMatrix = inverse(matrix, matrixSize)
        if inverseMatrix is not None:
            print "The inverse matrix is:"
            pretty_print_matrix(inverseMatrix, matrixSize)

    if (not calculateInverse and not calculateDeterminant):
        print "No operation specified, nothing do... have a nice day"

    sys.exit(0)

# Find determinant - a recursive function
def determinant(matrix, size):
    if size == 1:
        return matrix[0]

    value = 0
    mult = 1

    for i in range(0, size):
        value += mult*matrix[i]*determinant(get_submatrix(matrix, size, 0, i),size-1)
        mult *= -1

    return value

# Find inverse
def inverse(matrix, size):
    det = determinant(matrix, size)
    if det == 0:
        print "Inverse doesn't exist for the matrix:"
        pretty_print_matrix(matrix, size)
        return

    # Calculate inverse using matrix of minors, cofactors and adjugate
    inverseMatrix = inverse_cofactors(matrix, size, det)

    print "------------------------------------------------------------------------------------"
    print

    # Calculate using guass jordan elimination, set the boolean below to True when implemented
    inverseGJMethodImplemented = True
    inverseMatrixGJMethod = inverse_guass_jordan(matrix, size, det)

    # Check they are the same
    if inverseGJMethodImplemented:
        if matrices_are_same(inverseMatrix, inverseMatrixGJMethod):
            print "Yay! got the correct inverse using GJ method"
        else:
            print "Oops! got the wrong inverse using GJ method"

        print "Inverse via the GJ method:"
        pretty_print_matrix(inverseMatrixGJMethod, size)
        print
    else:
        print "Still need to implement inverse using GJ Method"

    print "------------------------------------------------------------------------------------"
    print

    return inverseMatrix

# Exercise: Remove the code for this function and the ones for both row reductions for stundets to implement
# This function should returns
#    1. The inverse of the matrix
#
# Inputs are
#    matrix: matrix to be inverted
#    size: size of the matrix e.g., 3 for a 3x3 matrix
#    det: determinant of the matrix (at this point it is guaranteed to be non-zero)
def inverse_guass_jordan(matrix, size, det):
    inverseMatrix = get_identity_matrix(size)

    print "Use Guass Jordan elimination and row-echelon form to find inverse of:"
    pretty_print_two_matrices(matrix, inverseMatrix, size)
    raw_input("Press Enter to continue...")
    print

    # Row reduce down to get to row-echelon form
    for i in range(0, size):
        if not is_identity_matrix(matrix, size):
            matrix, inverseMatrix = row_reduce_down(matrix, inverseMatrix, size, i)

        else:
            # found our inverse, return
            return inverseMatrix

    # Row reduce up to get inverse, last row already in proper form
    for i in range(size-1, 0, -1):
        if not is_identity_matrix(matrix, size):
            matrix, inverseMatrix = row_reduce_up(matrix, inverseMatrix, size, i-1)

        else:
            # found our inverse, return
            return inverseMatrix

    # At this point it should be the inverse
    return inverseMatrix

# Row reduction down - for Guass Jordan method. At the end of this matrix will be in row-echelon form
def row_reduce_down(m, inv, size, row):
    global step;
    if row > 0:
        step += 1
        hint = 0
        # Make all elements before the diagonal 0 by subtracting from rows above
        raw_input("Step %d: Make all elements in row %d, before column %d to be equal to 0. Press Enter when ready..."
                  % (step, row+1, row+1))
        for i in range(0, row):
            if m[row*size+i] != 0:
                e = m[row*size+i]
                if e != 1:
                    for j in range(0, size):
                        m[row*size+j] = m[row*size+j]/e
                        inv[row*size+j] = inv[row*size+j]/e
                    hint += 1
                    show_hint("    Hint %d.%d: Divide row %d by %.2f. Next..." % (step, hint, row+1, e), True, m, inv, size)

                for j in range(0, size):
                    m[row*size+j] = m[row*size+j]-m[i*size+j]
                    inv[row*size+j] = inv[row*size+j]-inv[i*size+j]
                hint += 1
                show_hint("    Hint %d.%d: Subtract row %d from row %d. Next..." % (step, hint, i+1, row+1), True, m, inv, size)

        if not showHint:
            pretty_print_two_matrices(m, inv, size)
            raw_input("Press Enter to continue...")
            print

    # Make the diagonal element 1
    if m[row*size+row] != 1:
        step += 1
        hint = 0
        raw_input("Step %d: Make the element in row %d, column %d to be equal to 1. Press Enter when ready..."
                  % (step, row+1, row+1))
        diagElement = m[row*size+row]

        # If the diagonal element is 0, need to add row with another whose corresponding column is non-zero
        # one such row is guaranteed to exist, otherwise determinant will be 0
        if diagElement == 0:
            # find row to add from
            for i in range(1, size):
                addRow = row+i
                if addRow >= size:
                    addRow -= size

                # Found the row to add from
                if m[addRow*size+row] != 0:
                    for k in range(0, size):
                        m[row*size+k] = m[row*size+k] + m[addRow*size+k]
                        inv[row*size+k] = inv[row*size+k] + inv[addRow*size+k]
                    hint += 1
                    show_hint("    Hint %d.%d: Add row %d to row %d. Next..." % (step, hint, addRow+1, row+1), True, m, inv, size)

                    diagElement = m[row*size+row]
                    break

        if diagElement != 0:
            for j in range(0, size):
                m[row*size+j] = m[row*size+j]/diagElement
                inv[row*size+j] = inv[row*size+j]/diagElement
            hint += 1
            show_hint("    Hint %d.%d: Divide row %d by %.2f. Next..." % (step, hint, row+1, diagElement), True, m, inv, size)

        if not showHint:
            pretty_print_two_matrices(m, inv, size)
            raw_input("Press Enter to continue...")
            print

    return m, inv

# Row reduction udown - for Guass Jordan method - at the end of this we will have inverse
def row_reduce_up(m, inv, size, row):
    global step;
    # Make all elements after the diagonal 0 by subtracting from rows below
    step += 1
    hint = 0
    raw_input("Step %d: Make all elements in row %d, after column %d to be equal to 0. Press Enter when ready..."
              % (step, row+1, row+1))
    for i in range(size-1, row, -1):
        if m[row*size+i] != 0:
            e = m[row*size+i]
            for j in range(0, size):
                m[row*size+j] -= m[i*size+j]*e
                inv[row*size+j] -= inv[i*size+j]*e
            if e != 1:
                hint += 1
                show_hint("    Hint %d.%d: Multiply row %d by: %.2f and subtract from row %d. Next..."
                          % (step, hint, i+1, e, row+1), True, m, inv, size)
            else:
                hint += 1
                show_hint("    Hint %d.%d: Subtract row %d from row %d. Next..." % (step, hint, i+1, row+1), True, m, inv, size)

    if not showHint:
        pretty_print_two_matrices(m, inv, size)
        raw_input("Press Enter to continue...")
        print

    return m, inv

# Inverse via minors, cofactors and adjugate - to double check Guass Jordan elimination
def inverse_cofactors(matrix, size, det):
    print "Calculate inverse using matrix of minors, cofactors and adjugate"
    print
    matrixMinors = []
    matrixCofactors = []
    mult1 = 1
    mult2 = 1
    for i in range(0, size):
        for j in range(0, size):
            minor = determinant(get_submatrix(matrix, size, i, j),size-1)
            matrixMinors.append(minor)

            cofactor = mult1*mult2*minor
            matrixCofactors.append(cofactor)

            mult2 *= -1
        mult1 *= -1
        mult2 = 1

    show_hint("Step 1: Find determinant of sub-matrices to get Matrix of Minors. Press Enter when ready...",
              True, matrixMinors, None, size)

    show_hint("Step 2: Alternate +/- on minors matrix to get Matrix of Cofactors. Press Enter when ready...",
              True, matrixCofactors, None, size)

    adjugateMatrix = transpose(matrixCofactors, size)
    show_hint("Step 3: Transpose the cofactors matrix to get Adjugate Matrix. Press Enter when ready...",
              True, adjugateMatrix, None, size)

    inverseMatrix = multiplyDeterminantInverse(adjugateMatrix, size, det) 
    show_hint("Step 4: Divide adjugate by determinant to get inverse Matrix. Press Enter when ready...",
               True, inverseMatrix, None, size)

    if not showHint:
        pretty_print_matrix(inverseMatrix, size)
        raw_input("Press Enter to continue...")
        print

    return inverseMatrix

# A bunch on utility functions below
def transpose(matrix, size):
    x = 0
    t = []
    for i in range(0, size):
        for j in range(0, size):
            x = i + j*size
            t.append(matrix[x])

    return t

def matrices_are_same(m1, m2):
    if len(m1) != len(m2):
        return False

    for i in range(0, len(m1)):
        if math.fabs(m1[i] - m2[i]) > 0.001:
            return False

    return True

def get_submatrix(m, size, row, column):
    matrix = []
    x = 0
    for i in range(0, size):
        for j in range(0, size):
            if i != row and j != column:
                matrix.append(m[x])
            x += 1

    return matrix

def multiplyDeterminantInverse(matrix, size, det):
    invDet = 1.0/det

    inv = []
    for e in matrix:
        x = e*invDet;
        inv.append(x)

    return inv

def get_identity_matrix(size):
    matrix = []
    x = 0
    for i in range(0, size):
        for j in range (0, size):
            if (i == j):
                matrix.append(1.0)
            else:
                matrix.append(0.0)

    return matrix

def is_identity_matrix(m, size):
    x = 0
    for i in range(0, size):
        for j in range(0, size):
            if i == j:
                if m[x] != 1.0: return False
            else:
                if m[x] != 0.0: return False
            x += 1

    return True

def get_largest_size(m, size):
    l = 2
    x = 0
    for i in range(0, size):
        for j in range(0, size):
            if len(str(m[x])) > l:
                l = len(str(m[x]))
            x += 1

    return l

def show_hint(s, prettyPrint, m1, m2, size):
    global showHint
    if showHint:
        raw_input(s)
        if prettyPrint:
            if m2 is not None:
                pretty_print_two_matrices(m1, m2, size)
                raw_input("    Press Enter to continue...")
            else:
                pretty_print_matrix(m1, size)
                raw_input("Press Enter to continue...")

            print

def pretty_print_matrix(matrix, size):
    m = []
    x = 0
    for i in range(0, size):
        for j in range(0, size):
            m.append("%.2f" % matrix[x])
            if m[x] == '-0.00':
                m[x] = '0.00'
            x += 1

    just = get_largest_size(m, size) + 1
    x = 0
    for i in range(0, size):
        for j in range(0, size):
            print m[x].rjust(just),
            x += 1
        print

def pretty_print_two_matrices(matrix1, matrix2, size):
    m1 = []
    m2 = []
    x = 0
    for i in range (0, size):
        for j in range(0, size):
            m1.append("%.2f" % matrix1[x])
            if m1[x] == '-0.00':
                m1[x] = '0.00'
            m2.append("%.2f" % matrix2[x])
            if m2[x] == '-0.00':
                m2[x] = '0.00'
            x += 1

    just1 = get_largest_size(m1, size) + 1
    just2 = get_largest_size(m2, size) + 1
    x1 = 0
    x2 = 0
    for i in range(0, size):
        for j in range(0, size):
            print m1[x1].rjust(just1),
            x1 += 1

        print "      ",
        for j in range(0, size):
            print m2[x2].rjust(just2),
            x2 += 1
        print

def parseArgs():
    global showHint
    matrix = ""
    calculateInverse = False
    calculateDeterminant = False

    # Get the inputs/arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vhidm:', ['matrix='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    # Parse the arguments
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-i', '--inverse'):
            calculateInverse = True
        elif opt in ('-d', '--determinant'):
            calculateDeterminant = True;
        elif opt in ('-v', '--verbose-hints'):
            showHint = True;
        elif opt in ('-m', '--matrix'):
            matrix = arg
        else:
            usage()
            sys.exit(2)

    if matrix == "":
        usage()
        sys.exit(2)

    return (calculateInverse, calculateDeterminant, matrix)

# Usage for this program
def usage():
    print sys.argv[0] + " [options]"
    print "Matrix is required:"
    print " -m MATRIX, --matrix MATRIX          Square matrix represented as a11,a12,...a1n,a21,a22,...,a2n,...,an1,an2,...ann"
    print "Options:"
    print " -i --inverse                        calculate the inverse of matrix"
    print " -d --determinant                    calculate the determinant of matrix"
    print " -v --verbose-hint                   show verbose hints for Guass Jordan elimination method"
    print " -h, --help                          show this help message and exit"

main()
