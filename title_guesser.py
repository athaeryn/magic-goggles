from __future__ import print_function

import os
import sys

from PIL import Image

from bktree import BKTree
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
        self._tree = BKTree(hamdist)
        # Don't include the last line, it's blank and blows things up.
        hashes = prep_hash_cache(file.read())[:-1]
        for h in hashes:
            self._tree.insert(h[0], meta={"name": h[1], "set": h[2]})
        file.close()

    # We're receiving a cropped card image (cv2, not PIL).
    def guess(self, img):
        # Convert cv2 image to PIL
        card = Image.fromarray(img)

        card_hash = get_hash(card)

        best_match = self._tree.query(card_hash, tolerance=2)

        return best_match
