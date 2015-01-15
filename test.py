from __future__ import print_function

import sys
import os
import argparse

import cv2

from vision import extract_title, ocr
from title_guesser import TitleGuesser


def _read_title_from_image(path):
    src = cv2.imread(path)
    title = extract_title(src.copy())
    ocr_guess = ocr(title)
    print("Tesseract says...", ocr_guess, file=sys.stderr)
    print(title_guesser.guess(ocr_guess))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", help="Image to read.", required=True)
    args = parser.parse_args()

    title_guesser = TitleGuesser(db_path=os.environ["CARD_DB_PATH"])

    if os.path.isfile(args.image):
        _read_title_from_image(args.image)
    else:
        print("Couldn't read file", file=sys.stderr)
        sys.exit(1)
