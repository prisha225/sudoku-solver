import cv2
import numpy as np


def preprocess(image_path):
    # Load the image
    img = cv2.imread(image_path)

    if img is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")

    # Convert to LAB color space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # Extract the Lightness (L) channel
    l_channel, _, _ = cv2.split(lab)

    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(l_channel, (9, 9), 1)

    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        15,
        4
    )

    # Morphological closing to connect broken grid lines
    kernel = np.ones((3, 3), np.uint8)

    thresh = cv2.morphologyEx(
        thresh,
        cv2.MORPH_CLOSE,
        kernel
    )

    return thresh


if __name__ == "__main__":

    image_path = "images/puzzle_yellow.png"

    try:
        thresh = preprocess(image_path)

        cv2.imshow("Thresholded Image", thresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        print(e)