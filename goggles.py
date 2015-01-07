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
from utils import drawers as draw
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
    """
    Draw the bounds on the image as rectangles.
    Returns the bounds.
    """
    card_bounds = _get_card_bounds(img)
    top_bounds = _get_top_bounds(img, card_bounds)
    title = _crop(img, top_bounds)

    blank = np.zeros(title.shape, dtype="uint8")
    gray = get.gray(title)
    blurred = cv2.medianBlur(gray, 3)
    draw.corners(blurred, blank, color=(255, 255, 255))
    blank = cv2.dilate(blank, None, iterations=2)

    title_bounds = _offset_bounds(_get_title_bounds(blank), top_bounds)

    _draw_bounds(img, top_bounds, colors["green"])
    _draw_bounds(img, card_bounds, colors["blue"], thickness=2)
    _draw_bounds(img, title_bounds, colors["red"], thickness=1)

    return {
        "card": card_bounds,
        "top": top_bounds,
        "title": title_bounds
    }


colors = {
    "white": (255, 255, 255),
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0)
}


def _process_title(frame, bounds):
    return _crop(frame, bounds)


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
            bounds = _process_frame(display_img)

            title = _crop(frame, bounds["title"])
            (h, w, _) = title.shape
            display_img[0:h, 0:w] = title

            cv2.imshow("goggles", display_img)
        except:
            cv2.imshow("goggles", display_img)
        if key == 27:  # Exit on escape.
            break
        elif key == 32:
            print("Trying to read title...", file=sys.stderr)
            try:
                title = _process_title(frame, bounds["title"])
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
        bounds = _process_frame(src.copy())
        title = _process_title(src, bounds["title"])
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
    cvimage = cv2.cvtColor(cvimage, cv2.COLOR_BGR2RGB)
    return image_to_string(Image.fromarray(cvimage)).replace("[", "")


# I'm planning to remove the --image arg, since this script should always be
# used with a webcam. The image option is still useful for testing if I don't
# have access to a webcam, so I'll make it a separate script.
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", help="The image to read.")
    args = parser.parse_args()

    title_guesser = TitleGuesser(db_path=os.environ["CARD_DB_PATH"])

    if args.image is None:
        _begin_webcam_loop()
    else:
        if os.path.isfile(args.image):
            _read_title_from_image(args.image)
        else:
            print("Couldn't read file", file=sys.stderr)
            sys.exit(1)
