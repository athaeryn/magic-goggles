#!/usr/bin/env python

import cv2
import numpy as np
from utils import getters as get
from utils import drawers as draw


def _crop(img, bounds):
    x1, y1, w, h = bounds
    x2 = x1 + w
    y2 = y1 + h
    return img[y1:y2, x1:x2]


def crop_to_card(img):
    gray = get.gray(img)
    blurred = cv2.medianBlur(gray, 9)
    thresh = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        15,
        4
    )
    bounds = get.bounds(get.contours(thresh))
    return _crop(img, bounds)


def crop_to_title(img):
    height = img.shape[0]
    width = img.shape[1]
    bounds = (0, 0, width, (height / 9))
    return _crop(img, bounds)


def highlight_bounds(img):
    w = img.shape[1]
    h = img.shape[0]

    top = h
    bottom = 0
    left = w
    right = 0

    gray = get.gray(img)

    for y in range(0, h):
        for x in range(0, w):
            if gray[y, x] == 255:
                if x > right:
                    right = x
                if x < left:
                    left = x
                if y > bottom:
                    bottom = y
                if y < top:
                    top = y

    return (left, top, right - left, bottom - top)


if __name__ == "__main__":
    src = cv2.imread("card.jpg")
    card = crop_to_card(src)
    title = crop_to_title(card)

    blank = np.zeros(title.shape, dtype="uint8")
    gray = get.gray(title)
    blurred = cv2.medianBlur(gray, 3)
    draw.corners(blurred, blank, color=(255, 255, 255))
    blank = cv2.dilate(blank, None, iterations=2)

    (x1, y1, w, h) = highlight_bounds(blank)
    cv2.rectangle(title, (x1, y1), (x1 + w, y1 + h), (0, 255, 0))

    cropped_title = get.gray(_crop(title, highlight_bounds(blank)))

    cv2.imshow("title", title)
    cv2.imwrite("tmp/title.jpg", cropped_title)
    cv2.waitKey(0)
