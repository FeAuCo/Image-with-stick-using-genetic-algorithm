import numpy as np
import cv2


def visualize(size, sticks, name='img', image=None):
    if image is None:
        new_img = np.ones(shape=size, dtype=np.uint8)*255  # создали белую картинку

        for stick in sticks:
            for pixel in stick.pixels:
                new_img[pixel[0], pixel[1]] = 0

        cv2.imshow(name, new_img)
        cv2.waitKey(0)
    else:
        for stick in sticks:
            for pixel in stick.pixels:
                image[pixel[0], pixel[1]] = 0

        cv2.imshow(name, image)
        cv2.waitKey(0)