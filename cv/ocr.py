import cv2
import pytesseract

from cv.grid import extract_grid
from cv.cells import extract_cells


def read_digit(cell):
    """
    Reads a single Sudoku cell.
    Returns:
        0 if the cell is empty
        The digit (1-9) if a digit is found.
    """

    # Count white pixels
    white_pixels = cv2.countNonZero(cell)
    total_pixels = cell.shape[0] * cell.shape[1]

    # Empty cell check
    if white_pixels / total_pixels < 0.05:
        return 0

    # OCR configuration
    config = "--psm 10 --oem 3 -c tessedit_char_whitelist=123456789"

    # Read the digit
    result = pytesseract.image_to_string(cell, config=config)

    # Remove spaces/newlines
    result = result.strip()

    # Return digit if valid
    if result.isdigit():
        return int(result)

    return 0


def read_board(cells):
    """
    Reads all 81 Sudoku cells and returns
    a 9x9 list of integers.
    """

    board = []

    for row in cells:

        board_row = []

        for cell in row:
            digit = read_digit(cell)
            board_row.append(digit)

        board.append(board_row)

    return board


if __name__ == "__main__":

    image_path = "images/puzzle.png"

    try:
        warped = extract_grid(image_path)

        cells = extract_cells(warped)

        board = read_board(cells)

        print("Detected Sudoku Board:\n")

        for row in board:
            print(row)

    except Exception as e:
        print(e)