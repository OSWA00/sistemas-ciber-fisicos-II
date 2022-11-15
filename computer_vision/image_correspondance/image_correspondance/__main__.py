import cv2 as cv
from harris import harris_detector

if __name__ == "__main__":

    paths = ["01.jpg", "02.png"]
    images = [cv.imread(f"data/{path}", 0) for path in paths]

    harris_images = [harris_detector(image, 0.7) for image in images]

    cv.destroyAllWindows()
