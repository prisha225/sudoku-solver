import cv2
from cv.grid import extract_grid


def extract_cells(warped, size=450):
    """
    Splits a warped Sudoku grid into 81 individual cells.
    Returns a 9x9 list of cell images.
    """

    cell_size = size // 9
    margin = 4

    cells = []

    for i in range(9):

        row = []

        for j in range(9):

            # Coordinates of the current cell
            y1 = i * cell_size
            y2 = (i + 1) * cell_size
            x1 = j * cell_size
            x2 = (j + 1) * cell_size

            # Remove the borders using a small margin
            cell = warped[
                y1 + margin:y2 - margin,
                x1 + margin:x2 - margin
            ]

            row.append(cell)

        cells.append(row)

    return cells


if __name__ == "__main__":

    image_path = "images/puzzle.png"

    try:
        warped = extract_grid(image_path)

        cells = extract_cells(warped)

        # Display the first cell
        cv2.imshow("Cell (0,0)", cells[3][0])

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        print(e)