#!/usr/bin/env python

from __future__ import print_function

import os
import os.path
import sys
import argparse
from uuid import uuid1 as uuid

import cv2
import Image
from pytesseract import image_to_string

from vision import extract_title
from title_guesser import TitleGuesser


colors = {
    "white": (255, 255, 255),
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0)
}


def _begin_webcam_loop():
    cv2.namedWindow("goggles")

    guess = ""

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
            title = extract_title(display_img)

            (h, w, _) = title.shape
            display_img[0:h, 0:w] = title

            cv2.putText(
                display_img,
                guess,
                (50, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0)
            )

            cv2.imshow("goggles", display_img)
        except:
            cv2.imshow("goggles", display_img)
        if key == 27:  # Exit on escape.
            break
        elif key == 112:  # Save frame on p.
            cv2.imwrite(str(uuid()) + ".jpg", frame)
        elif key == 32:  # Print guess on space.
            print(guess)
            guess = ""
        elif key == 103:  # Guess on g.
            print("Trying to read title...", file=sys.stderr)
            try:
                ocr_guess = ocr(title)
                print("Tesseract says...", ocr_guess, file=sys.stderr)
                guess = title_guesser.guess(ocr_guess)
                print(guess, file=sys.stderr)
                # print(title_guesser.guess(ocr_guess))
            except:
                pass

    cv2.destroyAllWindows()


# This function is mostly for testing.
def _read_title_from_image(path):
    src = cv2.imread(path)
    title = extract_title(src.copy())
    ocr_guess = ocr(title)
    print("Tesseract says...", ocr_guess, file=sys.stderr)
    print(title_guesser.guess(ocr_guess))


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

    title_guesser = TitleGuesser(db_path=os.environ["CARD_DB_PATH"])

    if args.image is None:
        _begin_webcam_loop()
    else:
        if os.path.isfile(args.image):
            _read_title_from_image(args.image)
        else:
            print("Couldn't read file", file=sys.stderr)
            sys.exit(1)
