import cv2
from preprocess import preprocess

def find_grid(image_path):

    # Get the thresholded image
    thresh = preprocess(image_path)

    # Find all contours
    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    print("Number of contours:", len(contours))

    # Find the largest contour
    largest = max(contours, key=cv2.contourArea)

    return thresh, largest


if __name__ == "__main__":

    image_path = "images/puzzle.png"

    thresh, largest = find_grid(image_path)

    # Convert to color so we can draw in green
    display = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    cv2.drawContours(display, [largest], -1, (0, 255, 0), 3)

    cv2.imshow("Largest Contour", display)

    cv2.waitKey(0)
    cv2.destroyAllWindows()