import cv2
import numpy as np
from cv.preprocess import preprocess


def warp_perspective(thresh, corners, size=450):
    """
    Takes a thresholded image and 4 ordered corner points,
    then returns a top-down square view of the Sudoku grid.
    """

    # Destination points (perfect square)
    dst = np.array([
        [0, 0],
        [size - 1, 0],
        [size - 1, size - 1],
        [0, size - 1]
    ], dtype="float32")

    # Compute transformation matrix
    matrix = cv2.getPerspectiveTransform(corners, dst)

    # Apply perspective transform
    warped = cv2.warpPerspective(thresh, matrix, (size, size))

    return warped


def extract_grid(image_path):

    # Preprocess the image
    thresh = preprocess(image_path)

    # Find contours
    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        raise ValueError("No contours found.")

    # Sort contours from largest to smallest
    contours = sorted(
        contours,
        key=cv2.contourArea,
        reverse=True
    )

    grid = None

    # Find the first contour that looks like a Sudoku grid
    for contour in contours:

        # Ignore tiny contours
        if cv2.contourArea(contour) < 1000:
            continue

        perimeter = cv2.arcLength(contour, True)

        approx = cv2.approxPolyDP(
            contour,
            0.02 * perimeter,
            True
        )

        # Get the bounding rectangle
        x, y, w, h = cv2.boundingRect(approx)

        # Calculate aspect ratio
        aspect_ratio = w / h

        # Accept only roughly square quadrilaterals
        if len(approx) == 4 and 0.9 <= aspect_ratio <= 1.1:
            grid = approx
            break

    # If no suitable contour was found
    if grid is None:
        raise ValueError("Could not detect a valid Sudoku grid.")

    # Convert to (4,2)
    corners = approx.reshape(4, 2)

    # Order corners
    ordered = np.zeros((4, 2), dtype="float32")

    s = corners.sum(axis=1)
    diff = np.diff(corners, axis=1)

    ordered[0] = corners[np.argmin(s)]      # Top-left
    ordered[2] = corners[np.argmax(s)]      # Bottom-right
    ordered[1] = corners[np.argmin(diff)]   # Top-right
    ordered[3] = corners[np.argmax(diff)]   # Bottom-left

    # Warp the Sudoku grid
    warped = warp_perspective(thresh, ordered)

    return warped

if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    thresh = preprocess(path)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest = max(contours, key=cv2.contourArea)
    display = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(display, [largest], -1, (0,255,0), 3)
    cv2.imshow("Largest contour", display)
    cv2.waitKey(0)

'''
if __name__ == "__main__":

    image_path = "images/puzzle.png"

    try:
        warped = extract_grid(image_path)

        cv2.imshow("Warped Sudoku", warped)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except ValueError as e:
        print(e)
        '''