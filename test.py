from __future__ import print_function

import os
import sys
from glob import glob

import cv2

from vision import extract_title
from ocr import ocr
from title_guesser import TitleGuesser


def _read_title_from_image(path):
    src = cv2.imread(path)
    title = extract_title(src.copy())
    ocr_guess = ocr(title)
    return title_guesser.guess(ocr_guess) if len(ocr_guess) > 0 else ""


if __name__ == "__main__":
    title_guesser = TitleGuesser("KTK")

    files = glob("./sample_imgs/*.jpg")
    files = map(lambda x: (x, os.path.splitext(os.path.basename(x))[0]), files)

    for path, name in files:
        try:
            guess = _read_title_from_image(path)
            if guess != name:
                print('Expected "{}" but got "{}"'.format(name, guess))
            else:
                print('Correctly guessed "{}"'.format(name))
        except:
            print('Error testing "{}": {}'.format(path, sys.exc_info()[0]))
