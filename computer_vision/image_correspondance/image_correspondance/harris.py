import cv2 as cv
import numpy as np


def harris_detector(img: np.array, threshold: float):
    img_copy = img.copy()

    dx = cv.Sobel(src=img_copy, ddepth=cv.CV_64F, dx=1, dy=0, ksize=5)
    dy = cv.Sobel(src=img_copy, ddepth=cv.CV_64F, dx=0, dy=1, ksize=5)
    dx_dy = cv.Sobel(src=img_copy, ddepth=cv.CV_64F, dx=1, dy=1, ksize=5)

    dx_2 = np.square(dx)
    dy_2 = np.square(dy)

    gauss_dx2 = cv.GaussianBlur(src=dx_2, ksize=(5, 5), sigmaX=0)
    gauss_dy2 = cv.GaussianBlur(src=dy_2, ksize=(5, 5), sigmaX=0)
    gauss_dx_dy = cv.GaussianBlur(src=dx_dy, ksize=(5, 5), sigmaX=0)

    detection = (
        gauss_dx2 * gauss_dy2
        - np.square(gauss_dx_dy)
        - 0.12 * np.square(gauss_dx2 + gauss_dy2)
    )

    cv.normalize(detection, detection, 0, 1, cv.NORM_MINMAX)

    loc = np.where(detection >= threshold)

    for point in zip(*loc[::-1]):
        cv.circle(img_copy, point, 3, (255, 255, 255), -1)

    cv.imshow("harris", img_copy)
    cv.waitKey(0)
