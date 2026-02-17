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

def kombinasiBarisGenerator(nTuple, length):
    """
    Generator untuk kombinasi tanpa menggunakan itertools.
    Menghasilkan kombinasi secara lazy untuk menghemat memori.
    """
    if length == 0:
        yield []
        return
    if len(nTuple) == 0:
        return

    for i in range(len(nTuple)):
        current = nTuple[i]
        sisa = nTuple[i+1:]
        for p in kombinasiBarisGenerator(sisa, length-1):
            yield [current] + p

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
    Optimized validation with early pruning.
    """
    usedColors = set()  # Use set for O(1) lookup

    for i in range(len(combination)):
        row, col = combination[i]
        color = matrix[row][col]

        # Early check: warna sudah dipakai
        if color in usedColors:
            return False
        usedColors.add(color)

        # Check conflicts dengan posisi sebelumnya
        for j in range(i):
            prev_row, prev_col = combination[j]

            # Same row or column
            if row == prev_row or col == prev_col:
                return False

            # Diagonal (distance 1)
            if abs(row - prev_row) == 1 and abs(col - prev_col) == 1:
                return False

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

