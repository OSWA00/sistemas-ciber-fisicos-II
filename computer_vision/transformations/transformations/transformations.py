"""Image transformations class implementation"""
from cmath import cos
from hashlib import new
import numpy as np


class Transformations:
    def __init__(self):
        pass

    def rotation(self, img, deg):
        """Rotates the image given a degree"""
        deg = np.deg2rad(deg)

        height, width, channels = img.shape

        new_img = np.zeros(img.shape)

        for x in range(0, width):
            for y in range(0, height):
                for z in range(0, channels):
                    new_x = int(x * np.cos(deg) - y * np.sin(deg))
                    new_y = int(x * np.sin(deg) + y * np.cos(deg))
                    new_img[new_x, new_y, z] = img[x, y, z]

        return new_img

    def flip_X(self, img):
        pass

    def flip_Y(self, img):
        pass

    def flip_X_Y(self, img):
        pass

    def translation(self, img, tx, ty):
        pass

    def scale(self, img, sx, sy):
        pass
