#!/usr/bin/env python

from __future__ import print_function

from uuid import uuid1 as uuid
import sys

import cv2

from vision import _get_cropped_card
from title_guesser import TitleGuesser


colors = {
    "white": (255, 255, 255),
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0)
}


def begin_webcam_loop():
    cv2.namedWindow("goggles")

    guess = ""
    frame_guess = ""

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

            frame_guess = guesser.guess(card)[1]

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

        except KeyboardInterrupt:
            sys.exit()
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
            print("WROTE:", guess, file=sys.stderr)
            print(guess)
            guess = ""
        elif key == 99:  # Clear guess on c.
            guess = ""
        elif key == 103:  # Guess on g.
            try:
                guess = frame_guess
                print("Locked:", guess, file=sys.stderr)
            except:
                pass

    cv2.destroyAllWindows()


if __name__ == "__main__":
    guesser = TitleGuesser()

    begin_webcam_loop()
