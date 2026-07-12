import cv2
import numpy as np


def preprocess(image_path):
    """
    Loads an image, converts it to grayscale,
    reduces noise, and returns a thresholded image.
    """

    # Load the image
    img = cv2.imread(image_path)

    # Check if the image was loaded successfully
    if img is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 1)

    # Apply Adaptive Thresholding
    thresh = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )

    # Close small gaps and remove tiny holes
    kernel = np.ones((3, 3), np.uint8)

    thresh = cv2.morphologyEx(
        thresh,
        cv2.MORPH_CLOSE,
        kernel
    )

    return thresh


# to test preprocessing
if __name__ == "__main__":

    image_path = "images/puzzle.png"

    try:
        processed = preprocess(image_path)

        cv2.imshow("Thresholded Sudoku", processed)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except FileNotFoundError as e:
        print(e)