from glob import glob
from PIL import Image

import cv2
import numpy as np
import imagehash

from vision import _gray

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


class TitleGuesser:
    def __self__(self):
        pass

    def load_set(self, set):
        files = glob("/Users/mike/magic/data/images/" + set + "/*.jpg")
        self.hashes = map(get_hash_path_pair_from_image_path, files)

    # Assume we're receiving a cropped card (cv) image.
    def guess(self, img):
        card = Image.fromarray(img)
        card_hash = get_hash(card)

        sorted_hashes = sorted(
            self.hashes,
            key=lambda (s_hash, _n): s_hash - card_hash
        )[:20]

        return get_name_from_path(sorted_hashes[0][1])
