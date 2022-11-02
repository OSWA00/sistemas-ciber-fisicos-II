"""Driver program"""

import os
import cv2 as cv
from transformations import Transformations


if __name__ == "__main__":
    rotation_config = [0, 90, 180, 270, 360]
    flip_translation_config = [[10, 10], [200, 200], [80, 0]]
    scale_config = [[1, 1], [0.5, 0.5], [2, 2]]

    TransformationHandler = Transformations()
    path = os.path.join("data", "logo.png")
    img = cv.imread(path)

    for rotation in rotation_config:
        rotated = TransformationHandler.rotation(img=img, deg=rotation)
        path = f"data/rotated/{rotation}.jpg"
        cv.imwrite(path, rotated)

    flipped_x = TransformationHandler.flip_x(img)
    path = f"data/flip_x/{0}.jpg"
    cv.imwrite(path, flipped_x)

    flipped_y = TransformationHandler.flip_y(img)
    path = f"data/flip_y/{0}.jpg"
    cv.imwrite(path, flipped_y)

    flipped_xy = TransformationHandler.flip_xy(img)
    path = f"data/flip_xy/{0}.jpg"
    cv.imwrite(path, flipped_xy)

    for translation in flip_translation_config:
        translated = TransformationHandler.translation(
            img, translation[0], translation[1]
        )
        path = f"data/translation/{translation[0]}X_{translation[1]}Y.jpg"
        cv.imwrite(path, translated)

    for scale in scale_config:
        scaled = TransformationHandler.scale(img, scale[0], scale[1])
        path = f"data/scaled/{scale[0]}X_{scale[1]}Y.jpg"
        cv.imwrite(path, scaled)

    cv.destroyAllWindows()
