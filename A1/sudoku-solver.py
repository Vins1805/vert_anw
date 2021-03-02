board=  [[8, 9, 0, 0, 0, 0, 0, 7, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 6], 
        [0, 0, 0, 2, 0, 7, 0, 0, 0], 
        [0, 0, 2, 0, 6, 0, 4, 0, 0], 
        [0, 0, 0, 9, 7, 2, 0, 0, 0], 
        [0, 0, 6, 0, 8, 0, 3, 0, 0], 
        [0, 0, 0, 5, 0, 1, 0, 0, 0], 
        [2, 0, 0, 0, 0, 0, 0, 0, 4], 
        [6, 5, 0, 0, 0, 0, 0, 8, 9]]
# die Zeile dazu ist
s = 890000071100000006000207000002060400000972000006080300000501000200000004650000089
  
def findNextCellToFill(board):
    for x in range(9):
        for y in range(9):
            if board[x][y] == 0:
                return x, y
    return -1, -1

def rowOK (board, i, j, e):
    for val in range(9):
        if e == board[i][val]: return False
    return True

def colOK (board, i, j, e):
    for val in range(9):
        if e == board[val][j]: return False
    return True

def isValid(board, i, j, e):
    if rowOK (board, i, j, e):
        if colOK (board, i, j, e):
            sX, sY = 3*(i//3), 3*(j//3)
            for x in range(sX, sX+3):
                for y in range(sY, sY+3):
                    if board[x][y] == e:
                        return False
            return True
    return False

def solveSudoku(board, i=0, j=0):
    i, j = findNextCellToFill(board)
    if i == -1:
        return True
    for e in range(1, 10):
        if isValid(board, i, j, e):
            board[i][j] = e
            if solveSudoku(board, i, j):
                return True
            board[i][j] = 0
    return False

def printSudoku(board):
    line = "+" + "-" * 7
    
    for i_row in range(len(board)):
        row = [str(i) for i in board[i_row]]

        if not i_row%3:
            print(line * 3 + "+")
        
        print("| " + " ".join(row[:3])
              + " | " + " ".join(row[3:6])
              + " | " + " ".join(row[6:])
              + " |")
        
    print(line * 3 + "+")
    
stringToBoard = lambda s: [[int(j) for j in str(s)[i:i+9]] for i in range(0, len(str(s)), 9)]

def readFile(filename='sudoku-Liste.txt') -> list:
    with open(filename, 'r') as reader:
        return [line.replace("\n", "") for line in reader.readlines() if not line.startswith("#")]
   
# TEILAUFGABE 4
solveSudoku(board)
printSudoku(board)

# TEILAUFGABE 5
print("String to Board")
board = stringToBoard(s)
solveSudoku(board)
printSudoku(board)

# TEILAUFGABE 6
sudokus = readFile()
counter = 1
for sudoku in sudokus:
    print("SUDOKU NR." + str(counter))
    board = stringToBoard(sudoku)
    printSudoku(board)
    solveSudoku(board)
    printSudoku(board)
    counter += 1

print("ende...")
