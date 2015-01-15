#!/usr/bin/env python

from __future__ import print_function

import os
import os.path
import sys
import argparse

import cv2
import numpy as np
import Image
from pytesseract import image_to_string

from utils import getters as get
from math import atan2, degrees
from title_guesser import TitleGuesser


def _crop(img, bounds):
    x1, y1, w, h = bounds
    x2 = x1 + w
    y2 = y1 + h
    return img[y1:y2, x1:x2]


def _offset_bounds(bounds, parent_bounds):
    (x, y, w, h) = bounds
    (px, py, pw, ph) = parent_bounds
    return (x + px, y + py, w, h)


def _get_card_bounds(img):
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
    return get.bounds(get.contours(thresh))


def get_contours(gray):
    blurred = cv2.medianBlur(gray, 3)
    edges = get.edges(blurred)
    contours, hierarchy = cv2.findContours(
        edges,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )
    return contours


def intersection(l1, l2):
    x1, y1, x2, y2 = l1
    x3, y3, x4, y4 = l2
    # http://en.wikipedia.org/wiki/Line-line_intersection#Given_two_points_on_each_line
    return (
        ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) /
        ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)),
        ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) /
        ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    )


def compute_angle(line):
    (x1, y1, x2, y2) = line
    (dx, dy) = (x2 - x1, y2 - y1)
    rads = atan2(-dy, dx)
    return abs(degrees(rads))


def compute_center(line):
    (x1, y1, x2, y2) = line
    return ((x1 + x2) / 2, (y1 + y2) / 2)


def get_cropped_card(img):
    gray = get.gray(img)
    blurred = cv2.medianBlur(gray, 17)

    edges = cv2.dilate(cv2.Canny(blurred, 100, 100, 3), None)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 200, 300, 100)[0]

    vert = filter(lambda l: abs(compute_angle(l) - 90) < 45, lines)
    hori = filter(lambda l: abs(compute_angle(l) - 0) < 45, lines)

    edges = [
        sorted(hori, key=lambda l: compute_center(l)[1])[0],   # top
        sorted(vert, key=lambda l: compute_center(l)[0])[0],   # left
        sorted(hori, key=lambda l: compute_center(l)[1])[-1],  # bottom
        sorted(vert, key=lambda l: compute_center(l)[0])[-1]   # right
    ]

    rect = np.zeros((4, 2), dtype="float32")
    rect[0] = intersection(edges[0], edges[1])  # top left
    rect[1] = intersection(edges[0], edges[3])  # top right
    rect[2] = intersection(edges[2], edges[3])  # bottom right
    rect[3] = intersection(edges[2], edges[1])  # bottom left

    width = 480
    height = 680

    dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype="float32")

    matrix = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(img, matrix, (width, height))

    return warped, edges


def _get_top_bounds(img, bounds):
    img = _crop(img, bounds)
    height = img.shape[0]
    width = img.shape[1]
    x_pad = int(width / 12.5)
    y_pad = height / 16
    return _offset_bounds((
        x_pad,
        y_pad,
        width - 5 * x_pad,
        int(height / 9.5) - y_pad
    ), bounds)


def _get_title_bounds(img):
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


def _draw_bounds(img, bounds, color=(255, 255, 255), thickness=1):
    (x, y, w, h) = bounds
    cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness)


def _process_frame(img):
    # small = cv2.pyrDown(img)
    small = img

    card, edges = get_cropped_card(small)

    for x1, y1, x2, y2 in edges:
        cv2.line(small, (x1, y1), (x2, y2), (0, 255, 0), 4)

    top = card[0:card.shape[1] / 5, 0:card.shape[0]]

    gray = get.gray(top)
    blurred = cv2.medianBlur(gray, 3)

    contours = get_contours(blurred)
    outer, _, inner = sorted(contours, key=cv2.contourArea, reverse=True)[:3]

    cv2.drawContours(top, [inner], -1, (255, 255, 255), 5)

    box = cv2.boundingRect(inner)
    title = _crop(top, box)

    gray = get.gray(title)
    _, thresh = cv2.threshold(gray, 140, 256, cv2.THRESH_BINARY)

    return thresh


colors = {
    "white": (255, 255, 255),
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0)
}


def _begin_webcam_loop():
    cv2.namedWindow("goggles")

    vc = cv2.VideoCapture(0)
    if vc.isOpened():  # Try to get the first frame.
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        rval, frame = vc.read()
        key = cv2.waitKey(33)
        frame = cv2.pyrDown(frame)
        display_img = frame.copy()
        try:
            title = _process_frame(display_img)

            (h, w, _) = title.shape
            display_img[0:h, 0:w] = title

            cv2.imshow("goggles", display_img)
        except:
            cv2.imshow("goggles", display_img)
        if key == 27:  # Exit on escape.
            break
        elif key == 32:  # Guess on space.
            print("Trying to read title...", file=sys.stderr)
            try:
                ocr_guess = ocr(title)
                print("Tesseract says...", ocr_guess, file=sys.stderr)
                print(title_guesser.guess(ocr_guess))
            except:
                pass

    cv2.destroyWindow("goggles")


# This function is mostly for testing.
def _read_title_from_image(path):
    src = cv2.imread(path)
    try:
        title = _process_frame(src.copy())
        ocr_guess = ocr(title)
        print("Tesseract says...", ocr_guess, file=sys.stderr)
        print(title_guesser.guess(ocr_guess))
    except:
        pass


def ocr(cvimage):
    """
    Run Tesseract on the title image in ./tmp.
    Returns the title as a string.
    """
    return image_to_string(Image.fromarray(cvimage)).replace("[", "")


# I'm planning to remove the --image arg, since this script should always be
# used with a webcam. The image option is still useful for testing if I don't
# have access to a webcam, so I'll make it a separate script.
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", help="The image to read.")
    args = parser.parse_args()

    title_guesser = TitleGuesser("KTK")

    if args.image is None:
        _begin_webcam_loop()
    else:
        if os.path.isfile(args.image):
            _read_title_from_image(args.image)
        else:
            print("Couldn't read file", file=sys.stderr)
            sys.exit(1)
