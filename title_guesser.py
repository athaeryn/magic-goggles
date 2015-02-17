from PIL import Image

from hasher import get_hash


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


def prep_hash_cache(file_contents):
    return map(
        lambda line: tuple(line.split("|")),
        file_contents.split("\n")
    )


class TitleGuesser:
    def __init__(self, hash_cache_path):
        file = open(hash_cache_path)
        # Don't include the last line, it's blank and blows things up.
        self._cache = prep_hash_cache(file.read())[:-1]
        file.close()

    # We're receiving a cropped card image (cv2, not PIL).
    def guess(self, img):
        card = Image.fromarray(img)
        card_hash = get_hash(card)

        best_match = sorted(
            self._cache,
            key=lambda (s_hash, _n, _s): hamdist(card_hash, s_hash)
        )[0]

        return best_match
