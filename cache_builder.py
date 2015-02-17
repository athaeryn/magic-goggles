from __future__ import print_function

import os
import sys
from glob import glob

from PIL import Image

from hasher import get_hash


def set_name_from_path(path):
    return path.split("/")[-1]


def card_name_from_path(path):
    return path.split("/")[-1].split(".")[0].lower()


def get_cache_text_for_set(path):
    set_name = set_name_from_path(path)

    cards = glob(os.path.join(path, "*.jpg"))

    hashes = map(
        lambda c: "|".join((
            get_hash(Image.open(c)),
            card_name_from_path(c),
            set_name
        )),
        cards
    )

    return "\n".join(hashes)


if __name__ == "__main__":
    images_path = os.environ["CARD_IMAGE_PATH"]

    if len(images_path) == 0:
        sys.exit

    sets = glob(os.path.join(images_path, "*"))

    cache = []

    for path in sets:
        cache.append(get_cache_text_for_set(path))

    print("\n".join(cache))
