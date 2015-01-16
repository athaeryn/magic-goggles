#!/usr/bin/env python

from __future__ import print_function

import sys
from uuid import uuid1 as uuid

import cv2

from vision import extract_title, ocr
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


if __name__ == "__main__":
    title_guesser = TitleGuesser("KTK")
    _begin_webcam_loop()
