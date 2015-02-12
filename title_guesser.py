from glob import glob
from PIL import Image

import cv2
import numpy as np
import imagehash

from vision import _gray

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
    w, h = img.size
    cropped = img.crop((10, 10, w - 10, h - 10 - h / 4))
    return str(imagehash.dhash(cropped)) + \
        str(imagehash.phash(cropped)) + \
        str(imagehash.average_hash(cropped))


# http://code.activestate.com/recipes/499304-hamming-distance/
def hamdist(str1, str2):
    """Count the # of differences between equal length strings str1 and str2"""
    diffs = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
            diffs += 1
    return diffs


def get_hash_path_pair_from_image_path(path):
    scan = Image.open(path)
    return (get_hash(scan), path)


def get_name_from_path(path):
    return path.split("/")[-1].split(".")[0].lower()


def get_closest_hash(card_hash):
    def match(scans):
        return sorted(
            scans,
            key=lambda (s_hash, _n): hamdist(card_hash, s_hash)
        )[0]
    return match


class TitleGuesser:
    def __init__(self):
        self._sets = []

    # Ideally we'll be loading all the sets, because of the hash cache.
    def load_set(self, set):
        files = glob("/Users/mike/magic/data/images/" + set + "/*.jpg")
        self._sets.append(map(get_hash_path_pair_from_image_path, files))

    # Assume we're receiving a cropped card (cv) image.
    def guess(self, img):
        card = Image.fromarray(img)
        card_hash = get_hash(card)

        matches = map(get_closest_hash(card_hash), self._sets)
        best_match = get_closest_hash(card_hash)(matches)

        return get_name_from_path(best_match[1])
