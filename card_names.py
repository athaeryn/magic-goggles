from __future__ import print_function
import os
import sys


def _sanitize_title(title):
    return title.replace(u'\xc6', "AE").encode("ascii", "ignore")


def load_card_names(sets):
    sets_txt_path = os.environ["SETS_TXT_PATH"]
    card_names = []
    for code in sets:
        try:
            path = os.path.join(sets_txt_path, code + ".txt")
            card_names += open(path).read().split("\n")
        except:
            print("Couldn't load set:", code, file=sys.stderr)

    return map(_sanitize_title, card_names)
