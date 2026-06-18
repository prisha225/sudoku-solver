def is_valid(board, row, col, num):

    # Checking for num across the same row
    for j in range(9):
        if board[row][j] == num:
            return False
        
    # Checking for num across the same column
    for i in range(9):
        if board[i][col] == num:
            return False
    
    # Checking all cells across 3x3 block
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3

    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    
    return True


def find_empty(board):
    
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i,j)
            
    return None


def solve(board):
    
    empty = find_empty(board)
    if empty is None:
        return True
    
    row, col = empty

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve(board):
                return True
            
            board[row][col] = 0

    return False

