import random
QUEENS_LABEL = "#"
def countWaranUnik(matrix):
    warnaUnik = set()
    for row in matrix:
        for color in row:
            warnaUnik.add(color)
    return len(warnaUnik)

def kombinasiBarisOptimal(n):
    if(len(n)<=1):
        return [n]
    result = []
    for i in range(len(n)):
        current = n[i]
        sisa = n[:i] + n[i+1:]
        for p in kombinasiBarisOptimal(sisa):
            result.append([current] + p)
    return result



def kombinasiBaris(nTuple, length):
    if length == 0:
        return [[]]
    if len(nTuple) == 0:
        return []
    result = []
    for i in range(len(nTuple)):
        sisa = nTuple[i+1:]
        for p in kombinasiBaris(sisa, length-1):
            result.append([nTuple[i]] + p)
    return result

def kombinasiBarisGenerator(nTuple, length, start=0):
    """
    Ultra-optimized generator dengan minimal overhead.
    Uses buffer approach instead of list concatenation.
    """
    n = len(nTuple)

    if length == 0:
        yield []
        return

    if start >= n or n - start < length:
        return

    # Single element case - fast path
    if length == 1:
        for i in range(start, n):
            yield [nTuple[i]]
        return

    # General case with optimized recursion
    for i in range(start, n - length + 1):
        current = nTuple[i]
        # Inline recursion result to avoid list concatenation overhead
        for suffix in kombinasiBarisGenerator(nTuple, length - 1, i + 1):
            # Optimized: extend existing list instead of concatenation
            result = [current]
            result.extend(suffix)
            yield result

def kombinasiBarisOptimalGenerator(n):
    """
    Generator untuk permutasi (mode optimal) secara lazy.
    Tidak menggunakan itertools.
    """
    if len(n) <= 1:
        yield n
        return

    for i in range(len(n)):
        current = n[i]
        sisa = n[:i] + n[i+1:]
        for p in kombinasiBarisOptimalGenerator(sisa):
            yield [current] + p

def hitungJumlahKombinasi(n, r):
    """
    Hitung C(n, r) = n! / (r! * (n-r)!)
    Untuk menampilkan total kombinasi yang akan dicek.
    """
    if r > n or r < 0:
        return 0
    if r == 0 or r == n:
        return 1

    # Optimasi: C(n,r) = C(n, n-r)
    r = min(r, n - r)

    result = 1
    for i in range(r):
        result = result * (n - i) // (i + 1)
    return result


def isPersegi(nRows, nCols):
    return nRows == nCols


def isValidCombinationOptimal(combination, matrix):

    usedColors = []
    for i in range(len(combination)):
        row = i
        col = combination[i]
        if matrix[row][col] in usedColors:
            return False
        for j in range(i):
            prev_row = j
            prev_col = combination[j]
            if abs(row - prev_row) == 1 and abs(col - prev_col) == 1:
                return False
            
        usedColors.append(matrix[row][col])
    return True


def isValidCombination(combination, matrix):
    """
    Ultra-optimized validation - squeeze every bit of performance!
    """
    n = len(combination)
    matrixSize = len(matrix)

    # Pre-allocate for speed - array access faster than set for N <= 20
    usedColors = set()
    usedRows = [False] * matrixSize
    usedCols = [False] * matrixSize  # Assumed square matrix

    # Process each position
    i = 0
    while i < n:
        row, col = combination[i]

        # Ultra fast row/col check with boolean array
        if usedRows[row] or usedCols[col]:
            return False

        # Color check
        color = matrix[row][col]
        if color in usedColors:
            return False

        # Diagonal check with aggressive early exit
        # Manual unrolling for first 2 positions (most common case)
        if i > 0:
            pr0, pc0 = combination[0]
            rd0 = row - pr0
            cd0 = col - pc0
            # Fast diagonal check: abs(diff) must be 1 for both
            if (rd0 == 1 or rd0 == -1) and (cd0 == 1 or cd0 == -1):
                return False

        if i > 1:
            pr1, pc1 = combination[1]
            rd1 = row - pr1
            cd1 = col - pc1
            if (rd1 == 1 or rd1 == -1) and (cd1 == 1 or cd1 == -1):
                return False

        # Check remaining queens (j >= 2)
        j = 2
        while j < i:
            prev_row, prev_col = combination[j]
            row_diff = row - prev_row
            col_diff = col - prev_col

            # Inlined check for maximum speed
            if (row_diff == 1 or row_diff == -1) and (col_diff == 1 or col_diff == -1):
                return False

            j += 1

        # Mark as used
        usedRows[row] = True
        usedCols[col] = True
        usedColors.add(color)

        i += 1

    return True

    

def print_matrix_optimal(matrix, combination=None):
    for i, row in enumerate(matrix):
        if combination is not None:
            row = list(row)
            row[combination[i]] = QUEENS_LABEL
        print(" ".join(row))

def print_matrix(matrix, combination=None):
    for i, row in enumerate(matrix):
        if combination is not None:
            row = list(row)
            for r, c in combination:
                if r == i:
                    row[c] = QUEENS_LABEL
        print(" ".join(row))

def generateRGB(char):
    colorMap = {
        'A': "#FF3434",  
        'B': "#9D71A8",  
        'C': '#45B7D1',  
        'D': '#FFA07A', 
        'E': '#98D8C8',  
        'F': '#F7DC6F',  
        'G': '#BB8FCE',  
        'H': '#85C1E2',  
        'I': '#F8B88B',  
        'J': '#82E0AA',  
        'K': '#F1948A',  
        'L': '#AED6F1',  
        'M': '#F5B041',  
        'N': '#D7BDE2',  
        'O': '#76D7C4',  
        'P': '#F9E79F', 
        'Q': '#F8B195',  #
        'R': '#C5E1A5',  
        'S': '#FFD89B',  
        'T': '#B19CD9',  
        'U': '#80DEEA', 
        'V': '#FF8A65',  
        'W': '#81C784',
        'X': '#BA68C8',  
        'Y': '#FFD54F', 
        'Z': '#64B5F6',  
    }
    return colorMap.get(char, '#CCCCCC') 



def isKotakSamaWarna(matrix):
    nWarnaUnik = countWaranUnik(matrix)
    nRows = len(matrix)
    if nWarnaUnik != nRows:
        return False
    return True
#============================================================

