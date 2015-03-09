from __future__ import print_function

import os
import sys

from PIL import Image

from hamdist import hamdist
from hasher import get_hash


def get_hash_path_pair_from_image_path(path):
    scan = Image.open(path)
    return (get_hash(scan), path)


def get_name_from_path(path):
    return path.split("/")[-1].split(".")[0].lower()


def prep_hash_cache(file_contents):
    return map(
        lambda line: tuple(line.split("|")),
        file_contents.split("\n")
    )


class TitleGuesser:
    def __init__(self):
        try:
            file = open(os.environ["CARD_HASH_CACHE"])
        except:
            print("CARD_HASH_CACHE not set!", file=sys.stderr)
            exit(1)
        # Don't include the last line, it's blank and blows things up.
        self._cache = prep_hash_cache(file.read())[:-1]
        file.close()

    # We're receiving a cropped card image (cv2, not PIL).
    def guess(self, img):
        # Convert cv2 image to PIL
        card = Image.fromarray(img)

        card_hash = get_hash(card)

        best_match = sorted(
            self._cache,
            key=lambda (s_hash, _n, _s): hamdist(card_hash, s_hash)
        )[0]

        return best_match
