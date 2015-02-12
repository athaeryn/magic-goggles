#!/usr/bin/env python

from __future__ import print_function

import sys
from uuid import uuid1 as uuid

import cv2

from vision import _get_cropped_card
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

        if len(guess) > 0:
            guess_display_text = "will write: " + guess
        else:
            guess_display_text = ""

        try:
            card = _get_cropped_card(display_img)

            frame_guess = guesser.guess(card)

            cv2.putText(
                display_img,
                frame_guess,
                (50, 100),
                cv2.FONT_HERSHEY_PLAIN,
                1,
                colors["red"]
            )
            cv2.putText(
                display_img,
                guess_display_text,
                (50, 200),
                cv2.FONT_HERSHEY_PLAIN,
                1,
                colors["blue"]
            )

            cv2.imshow("goggles", display_img)

        except:
            cv2.putText(
                display_img,
                guess_display_text,
                (50, 200),
                cv2.FONT_HERSHEY_PLAIN,
                1,
                colors["blue"]
            )
            cv2.imshow("goggles", display_img)
        if key == 27:  # Exit on escape.
            break
        elif key == 112:  # Save frame on p.
            cv2.imwrite(str(uuid()) + ".jpg", frame)
        elif key == 32:  # Print guess on space.
            print(guess)
            guess = ""
        elif key == 99:  # Clear guess on c.
            guess = ""
        elif key == 103:  # Guess on g.
            print("Locking in guess...", file=sys.stderr)
            try:
                guess = guesser.guess(card)
                print(guess, file=sys.stderr)
            except:
                pass

    cv2.destroyAllWindows()


if __name__ == "__main__":
    sets = [
        "DGM",
        "BNG",
        "JOU",
        "THS",
        "RTR",
        "GTC",
        "KTK",
        "FRF",
        "M14",
        "M15"
    ]
    guesser = TitleGuesser()

    for set in sets:
        guesser.load_set(set)

    _begin_webcam_loop()
