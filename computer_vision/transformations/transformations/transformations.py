"""Image transformations class implementation"""
import numpy as np


class Transformations:
    def __init__(self):
        pass

    def rotation(self, img, deg):
        """Rotates the image given a degree"""
        deg = np.deg2rad(deg)

        height, width, channels = img.shape

        new_img = np.zeros(img.shape)

        for x_cor in range(0, width):
            for y_cor in range(0, height):
                for z_cor in range(0, channels):
                    new_x = int(x_cor * np.cos(deg) - y_cor * np.sin(deg))
                    new_y = int(x_cor * np.sin(deg) + y_cor * np.cos(deg))
                    new_img[new_x, new_y, z_cor] = img[x_cor, y_cor, z_cor]

        return new_img

    def flip_x(self, img):
        """Flips image over X axis"""
        height, width, channels = img.shape

        new_img = np.zeros(img.shape)

        for x_cor in range(0, width):
            for y_cor in range(0, height):
                for z_cor in range(0, channels):
                    new_x = x_cor
                    new_y = -y_cor
                    new_img[new_x, new_y, z_cor] = img[x_cor, y_cor, z_cor]

        return new_img

    def flip_y(self, img):
        """Flips image over Y axis"""
        height, width, channels = img.shape

        new_img = np.zeros(img.shape)

        for x_cor in range(0, width):
            for y_cor in range(0, height):
                for z_cor in range(0, channels):
                    new_x = -x_cor
                    new_y = y_cor
                    new_img[new_x, new_y, z_cor] = img[x_cor, y_cor, z_cor]

        return new_img

    def flip_xy(self, img):
        """Flips image over Y and X axis"""
        height, width, channels = img.shape

        new_img = np.zeros(img.shape)

        for x_cor in range(0, width):
            for y_cor in range(0, height):
                for z_cor in range(0, channels):
                    new_x = y_cor
                    new_y = x_cor
                    new_img[new_x, new_y, z_cor] = img[x_cor, y_cor, z_cor]

        return new_img

    def translation(self, img, tx, ty):
        height, width, channels = img.shape
        new_img = np.zeros((height + tx, width + ty, channels))

        for x_cor in range(0, width):
            for y_cor in range(0, height):
                for z_cor in range(0, channels):
                    new_x = x_cor + tx
                    new_y = y_cor + ty
                    new_img[new_x, new_y, z_cor] = img[x_cor, y_cor, z_cor]


        return new_img

    def scale(self, img, sx, sy):
        pass
