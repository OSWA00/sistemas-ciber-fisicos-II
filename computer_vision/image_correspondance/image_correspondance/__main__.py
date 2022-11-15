import cv2 as cv
import numpy as np
from harris import harris_detector

if __name__ == "__main__":

    paths = ["01.jpg", "02.png"]
    images = [cv.imread(f"data/{path}", 0) for path in paths]

    harris_detection = [harris_detector(image) for image in images]
    harris_images = []

    for image, detection in zip(images, harris_detection):
        img_copy = image.copy()
        threshold = 0.7
        loc = np.where(detection >= threshold)  #! Maybe this is important

        for point in zip(*loc[::-1]):
            cv.circle(img_copy, point, 3, (255, 255, 255), -1)

        harris_images.append(img_copy)
        cv.imshow("harris", img_copy)
        cv.waitKey(0)

        cv.destroyAllWindows()
