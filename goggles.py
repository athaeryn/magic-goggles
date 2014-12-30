#!/usr/bin/env python

import cv2

import numpy as np

from utils import getters as get
from utils import drawers as draw


def crop(img):
    x1,y1,w,h = get.bounds(get.contours(get.gray(img)))
    x2 = x1 + w
    y2 = y1 + (h / 8)
    x1 += w / 25
    y1 += h / 25
    return img[y1:y2, x1:x2]


if __name__ == "__main__":

    src = cv2.imread("card.jpg")
    card_img = get.gray(crop(src))

    cv2.imshow("title", card_img)
    cv2.imwrite("title.jpg", card_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
