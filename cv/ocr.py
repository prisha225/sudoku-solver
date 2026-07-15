from digit_model.predict import predict_digit
from cv.grid import extract_grid
from cv.cells import extract_cells


def read_digit(cell):
    """
    Reads a single Sudoku cell using the CNN.
    """

    return predict_digit(cell)


def read_board(cells):
    """
    Reads all 81 Sudoku cells and returns
    a 9x9 Sudoku board.
    """

    board = []

    for row in cells:

        board_row = []

        for cell in row:
            board_row.append(read_digit(cell))

        board.append(board_row)

    return board


if __name__ == "__main__":

    image_path = "images/puzzle_yellow.png"

    try:
        warped = extract_grid(image_path)

        cells = extract_cells(warped)

        board = read_board(cells)

        print("Detected Sudoku Board:\n")

        for row in board:
            print(row)

    except Exception as e:
        print(e)