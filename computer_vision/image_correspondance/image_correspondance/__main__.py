import cv2 as cv
import numpy as np
from harris import harris_detector
from homography_estimation import compute_image_correspondance

if __name__ == "__main__":

    paths = ["01.jpg", "02.png"]
    images = [cv.imread(f"data/{path}", cv.IMREAD_GRAYSCALE) for path in paths]

    Harris corner detection
    for index, image in enumerate(images):
        img_copy = image.copy()
        detection = harris_detector(image)

        threshold = 0.7
        loc = np.where(detection >= threshold)

        for point in zip(*loc[::-1]):
            cv.circle(img_copy, point, 3, (255, 255, 255), -1)

        path = f"data/harris/harris_{index}.png"
        cv.imwrite(path, img_copy)

    # Homography estimation
    compute_image_correspondance(images[0], images[1])

    cv.destroyAllWindows()
