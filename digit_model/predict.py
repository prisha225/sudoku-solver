import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load the model only once
model = load_model("digit_model/mnist_model.keras")


def predict_digit(cell_img):
    """
    Predicts the digit in a Sudoku cell.

    Returns:
        0 if the cell is empty
        Digit (1-9) otherwise
    """

    # Check if the cell is empty
    white_pixels = cv2.countNonZero(cell_img)
    total_pixels = cell_img.shape[0] * cell_img.shape[1]

    # Slightly stricter empty-cell threshold
    if white_pixels / total_pixels < 0.08:
        return 0

    # Find all white pixels (the digit)
    coords = cv2.findNonZero(cell_img)

    # Safety check
    if coords is None:
        return 0

    # Crop tightly around the digit
    x, y, w, h = cv2.boundingRect(coords)
    digit = cell_img[y:y+h, x:x+w]

    # Add padding around the digit
    pad = 4
    digit = cv2.copyMakeBorder(
        digit,
        pad,
        pad,
        pad,
        pad,
        cv2.BORDER_CONSTANT,
        value=0
    )

    # Resize to MNIST dimensions
    digit = cv2.resize(digit, (28, 28))

    # Normalize pixel values
    digit = digit.astype("float32") / 255.0

    # Add channel dimension
    digit = np.expand_dims(digit, axis=-1)

    # Add batch dimension
    digit = np.expand_dims(digit, axis=0)

    # Predict
    prediction = model.predict(digit, verbose=0)

    # Return the most likely digit
    return int(np.argmax(prediction))