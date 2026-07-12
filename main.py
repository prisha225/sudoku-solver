from cv.grid import extract_grid
from cv.cells import extract_cells
from cv.ocr import read_board

from solver.solve import solve
from solver.board import print_board

image_path = "images/puzzle.png"

warped = extract_grid(image_path)
cells = extract_cells(warped)
board = read_board(cells)

print("Detected Puzzle:")
print_board(board)

if solve(board):
    print("\nSolved Puzzle:")
    print_board(board)
else:
    print("No solution exists.")