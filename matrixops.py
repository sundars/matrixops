import getopt, sys, math

step = 0
showHint = False

def main():
    global showHint
    calculateInverse, calculateDeterminant, m1, r1, c1, m2, r2, c2 = parseArgs()

    print
    if r2 != 0 and c2 != 0:
        print "Input matrices are:"
        pretty_print_two_matrices(m1, m2, r1, c1, r2, c2)
        print
        if calculateDeterminant: print "- Calculate determinant of first matrix"
        if calculateInverse: print "- Calculate inverse of first matrix"
        print "- Left multiply second matrix with the first matrix"
    else:
        print "Input matrix is:"
        pretty_print_matrix(m1, r1, c1)
        print
        if calculateDeterminant: print "- Calculate determinant of this matrix"
        if calculateInverse: print "- Calculate inverse of this matrix"
    print
    print "------------------------------------------------------------------------------------"
    print

    if calculateDeterminant:
        det = determinant(m1, r1)
        print "Determinant = ", det
        print
        print "------------------------------------------------------------------------------------"
        print

    if calculateInverse:
        inverseMatrix = inverse(m1, r1)
        if inverseMatrix is not None:
            print "The inverse matrix is:"
            pretty_print_matrix(inverseMatrix, r1)
            print
            print "------------------------------------------------------------------------------------"
            print

        print "Multiplying a matrix and its inverse will give..."
        pretty_print_two_matrices(m1, inverseMatrix, r1)
        raw_input("Press Enter to continue...")
        print
        tmp = showHint
        showHint = False
        productMatrix = multiply(m1, inverseMatrix, r1)
        showHint = tmp
        if not is_identity_matrix(productMatrix, r1):
            print "Something went wrong..."
            pretty_print_matrix(productMatrix, r1)
            sys.exit(4)

        print "The identity matrix:"
        pretty_print_matrix(productMatrix, r1)
        print
        print "------------------------------------------------------------------------------------"
        print

    if r2 != 0 and c2 != 0:
        if c1 != r2:
            print "Cannot multiply these two matrices:"
            pretty_print_two_matrices(m1, m2, r1, c1, r2, c2)
            sys.exit(5)

        print "Multiply the following two matrices:"
        pretty_print_two_matrices(m1, m2, r1, c1, r2, c2)
        raw_input("Press Enter to continue...")
        print
        productMatrix = multiply(m1, m2, r1, c1, r2, c2)
        print "Product matrix:"
        pretty_print_matrix(productMatrix, r1, c2)
        print
        print "------------------------------------------------------------------------------------"
        print


    if (not calculateInverse and not calculateDeterminant and (r2 == 0 or c2 == 0)):
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

# Exercise: Remove the code for this function and the ones for both row reduction functions below for students to implement
# This function should return
#    1. The inverse of the matrix
#
# Inputs are
#    matrix: matrix to be inverted
#    size: size of the matrix e.g., 3 for a 3x3 matrix
#    det: determinant of the matrix (at this point it is guaranteed to be non-zero)
def inverse_guass_jordan(m, size, det):
    # Make a copy - python is effectively pass by reference
    matrix = []
    for i in range(0, size*size):
        matrix.append(m[i])

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
    global step
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

        if hint == 0 or not showHint:
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

        if hint == 0 or not showHint:
            pretty_print_two_matrices(m, inv, size)
            raw_input("Press Enter to continue...")
            print

    return m, inv

# Row reduction up - for Guass Jordan method - at the end of this we will have inverse
def row_reduce_up(m, inv, size, row):
    global step
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

    if hint == 0 or not showHint:
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
        print "Inverse is:"
        pretty_print_matrix(inverseMatrix, size)
        raw_input("Press Enter to continue...")
        print

    return inverseMatrix

# Matrix multiplication - m2 left multiplied by m1
# Input two matrices and their sizes: r1, c1, r2, c2
# Either only r1 is specified in which case it is 2 square matrices of same size
# Or all 4 sizes are specified
#
# Output is the product of the two matrices
def multiply(m1, m2, r1, c1=-1, r2=-1, c2=-1):
    if c1 == -1:
        # Two square matrix of same size
        c1 = r2 = c2 = r1

    if c1 != r2:
        # Two square matrices of different size, cannot multiply
        return None

    matrix = []
    for i in range(0, r1):
        for j in range(0, c2):
            matrix.append('...')

    x = 0
    for i in range(0, r1):
        for j in range(0, c2):
            e = 0
            for k in range(0, c1):
                e += m1[i*c1+k]*m2[k*c2+j]
            matrix[x] = e
            x += 1
            show_hint("Step %d: Multiply corresponding elements in row %d of 1st matrix and column %d of 2nd matrix and add up..."
                      % (x, i+1, j+1), True, matrix, None, r1, c2)

    return matrix

# A bunch of utility functions below
# Only valid for square matrix
def transpose(matrix, size):
    x = 0
    t = []
    for i in range(0, size):
        for j in range(0, size):
            x = i + j*size
            t.append(matrix[x])

    return t

# Any 2 matrices
def matrices_are_same(m1, m2):
    if len(m1) != len(m2):
        return False

    for i in range(0, len(m1)):
        if math.fabs(m1[i] - m2[i]) > 0.001:
            return False

    return True

# Only valid for square matrix
def get_submatrix(m, size, row, column):
    matrix = []
    x = 0
    for i in range(0, size):
        for j in range(0, size):
            if i != row and j != column:
                matrix.append(m[x])
            x += 1

    return matrix

# Only valid for square matrix
def multiplyDeterminantInverse(matrix, size, det):
    invDet = 1.0/det

    inv = []
    for e in matrix:
        x = e*invDet
        inv.append(x)

    return inv

# Only valid for square matrix
def get_identity_matrix(size):
    matrix = []
    for i in range(0, size):
        for j in range (0, size):
            if (i == j):
                matrix.append(1.0)
            else:
                matrix.append(0.0)

    return matrix

# Only valid for square matrix
def is_identity_matrix(m, size):
    x = 0
    for i in range(0, size):
        for j in range(0, size):
            if i == j:
                if m[x]-1.0 > 0.001: return False
            else:
                if m[x]-0.0 > 0.001: return False
            x += 1

    return True

# Input matrix and size: r1, c1
# If c1 is -1, it is a square matrix
def get_largest_size(m, rSize, cSize):
    l = 2
    x = 0
    for i in range(0, rSize):
        for j in range(0, cSize):
            if len(str(m[x])) > l:
                l = len(str(m[x]))
            x += 1

    return l

# Input two matrices and their sizes: r1, c1, r2, c2
# Either only r1 is specified in which case it is 2 square matrices of same size
# Or all 4 sizes are specified
def show_hint(s, prettyPrint, m1, m2, rSize1, cSize1=-1, rSize2=-1, cSize2=-1):
    if cSize1 == -1:
        # Two square matrices of same size
        cSize1 = rSize2 = cSize2 = rSize1

    global showHint
    if showHint:
        raw_input(s)
        if prettyPrint:
            if m2 is not None:
                pretty_print_two_matrices(m1, m2, rSize1, cSize1, rSize2, cSize2)
            else:
                pretty_print_matrix(m1, rSize1, cSize1)

            raw_input("Press Enter to continue...")
            print

# Input matrix and size: r1, c1
# If c1 is -1, it is a square matrix
def pretty_print_matrix(matrix, rSize, cSize=-1):
    if cSize == -1:
        # Square matrix
        cSize = rSize

    m = []
    x = 0
    for i in range(0, rSize):
        for j in range(0, cSize):
            if type(matrix[x]) is str:
                m.append(matrix[x])
            else:
                m.append("%.2f" % matrix[x])
            if m[x] == '-0.00':
                m[x] = '0.00'
            x += 1

    just = get_largest_size(m, rSize, cSize) + 1
    x = 0
    for i in range(0, rSize):
        for j in range(0, cSize):
            print m[x].rjust(just),
            x += 1
        print

# Input two matrices and their sizes: r1, c1, r2, c2
# Either only r1 is specified in which case it is 2 square matrices of same size
# Or all 4 sizes are specified
def pretty_print_two_matrices(matrix1, matrix2, rSize1, cSize1=-1, rSize2=-1, cSize2=-1):
    if cSize1 == -1:
        # Two square matrices of same size
        cSize1 = rSize2 = cSize2 = rSize1

    m1 = []
    x = 0
    for i in range (0, rSize1):
        for j in range(0, cSize1):
            if type(matrix1[x]) is str:
                m1.append(matrix1[x])
            else:
                m1.append("%.2f" % matrix1[x])
            if m1[x] == '-0.00':
                m1[x] = '0.00'
            x += 1

    m2 = []
    x = 0
    for i in range (0, rSize2):
        for j in range(0, cSize2):
            if type(matrix2[x]) is str:
                m2.append(matrix2[x])
            else:
                m2.append("%.2f" % matrix2[x])
            if m2[x] == '-0.00':
                m2[x] = '0.00'
            x += 1

    just1 = get_largest_size(m1, rSize1, cSize1) + 1
    just2 = get_largest_size(m2, rSize2, cSize2) + 1
    x1 = 0
    x2 = 0
    for i in range(0, max(rSize1, rSize2)):
        for j in range(0, cSize1):
            if i < rSize1:
                print m1[x1].rjust(just1),
                x1 += 1
            else:
                print ''.rjust(just1),

        print "      ",
        for j in range(0, cSize2):
            if i < rSize2:
                print m2[x2].rjust(just2),
                x2 += 1
            else:
                print ''.rjust(just2),
        print

def parseArgs():
    global showHint
    marg = ""
    parg = ""
    calculateInverse = False
    calculateDeterminant = False

    # Get the inputs/arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vhidp:m:', ['matrix=', 'matrix-multiply='])
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
            calculateDeterminant = True
        elif opt in ('-v', '--verbose-hints'):
            showHint = True
        elif opt in ('-m', '--matrix'):
            marg = arg
        elif opt in ('-p', '--matrix-multiply'):
            parg = arg
        else:
            usage()
            sys.exit(2)

    if marg == "":
        usage()
        sys.exit(2)

    # Parse the matrices
    m1 = []
    r1 = 0
    c1 = 0
    rows = marg.split(':')
    if len(rows) == 1:
        # Assume square matrix
        for e in marg.split(','):
            m1.append(float(e))

        r1 = c1 = int(math.sqrt(len(m1)))
        if r1 ** 2 != len(m1):
            print "Expected a square matrix for -m argument"
            print "If non-square, specify as a11,a12,...a1n:a21,a22,...a2n:...:am1,am2...amn:"
            usage()
            sys.exit(3)

    else:
        r1 = len(rows)
        if rows[r1-1] == "":
            r1 -= 1
        for i in range(0, r1):
            for e in rows[i].split(','):
                m1.append(float(e))

        c1 = int(len(m1)/r1)
        if c1*r1 != len(m1):
            print "Matrix with -m isn't properly formatted"
            print "Format as a11,a12,...,a1n:a21,a22,...,a2n:...:am1,am2,...,amn:"
            usage()
            sys.exit(3)

    if (calculateInverse or calculateDeterminant) and (r1 != c1):
        print "Must specify square matrix to calculate inverse or determinant"
        usage()
        sys.exit(3)

    m2 = []
    r2 = 0
    c2 = 0
    if parg is not "":
        rows = parg.split(':')
        if len(rows) == 1:
            # Assume square matrix
            for e in parg.split(','):
                m2.append(float(e))

            c2 = r2 = int(math.sqrt(len(m2)))
            if r2 ** 2 != len(m2):
                print "Expected a square matrix for -p argument"
                print "If non-square, specify as a11,a12,...,a1n:a21,a22,...,a2n:...:am1,am2,...,amn:"
                usage()
                sys.exit(3)

        else:
            r2 = len(rows)
            if rows[r2-1] == "":
                r2 -= 1
            for i in range(0, r2):
                for e in rows[i].split(','):
                    m2.append(float(e))

            c2 = int(len(m2)/r2)
            if c2*r2 != len(m2):
                print "Matrix with -p isn't properly formatted"
                print "Format as a11,a12,...,a1n:a21,a22,...,a2n:...:am1,am2,...,amn:"
                usage()
                sys.exit(3)

    return (calculateInverse, calculateDeterminant, m1, r1, c1, m2, r2, c2)

# Usage for this program
def usage():
    print
    print sys.argv[0] + " [options]"
    print "Matrix is required:"
    print " -m MATRIX, --matrix=MATRIX          Square matrix formatted as a11,a12,...,a1n,a21,a22,...,a2n,...,an1,an2,...,ann"
    print "                                     Non-square formatted as a11,a12,...,a1n:a21,a22,...,a2n:...:am1,am2,...,amn:"
    print "Options:"
    print " -p MATRIX --matrix-multiply=MATRIX  left multiply matrix provided by -m with the one provided by -p"
    print " -i --inverse                        calculate the inverse of matrix"
    print " -d --determinant                    calculate the determinant of matrix"
    print " -v --verbose-hint                   show verbose hints for Guass Jordan elimination method"
    print " -h, --help                          show this help message and exit"

main()
