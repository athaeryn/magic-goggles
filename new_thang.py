from __future__ import print_function

from glob import glob

import cv2
import imagehash
import numpy as np
from PIL import Image

from vision import _get_cropped_card, _gray

hash_func = imagehash.dhash

size = (128, 128)


def process_img(pilimg):
    pilimg = pilimg.resize(size, Image.ANTIALIAS)
    img = np.array(pilimg)

    img = _gray(img)
    img = cv2.medianBlur(img, 3)
    img = cv2.equalizeHist(img)

    return Image.fromarray(img)


def get_hash(img):
    img = process_img(img)
    return hash_func(img)


def get_hash_path_pair_from_image_path(path):
    scan = Image.open(path)
    return (get_hash(scan), path)


def get_name_from_path(path):
    return path.split("/")[-1].split(".")[0].lower()


if __name__ == "__main__":
    files = glob("/Users/mike/magic/data/images/KTK/*.jpg")
    hashes = map(get_hash_path_pair_from_image_path, files)

    cards = glob("./sample_imgs/*.jpg")

    for path in cards:
        card_name = get_name_from_path(path)

        img = Image.open(path)
        card = Image.fromarray(_get_cropped_card(np.array(img)))
        img_hash = get_hash(card)

        sorted_hashes = sorted(
            hashes,
            key=lambda (s_hash, _n): s_hash - img_hash
        )[:20]

        best_guess = get_name_from_path(sorted_hashes[0][1])

        if card_name == best_guess:
            print(" ", card_name)
        else:
            print("X", card_name, "(guessed: " + best_guess + ")")
