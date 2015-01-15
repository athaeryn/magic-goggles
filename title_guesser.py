from __future__ import print_function
import sys

from fuzzywuzzy import process

from card_names import load_card_names


class TitleGuesser:
    def __init__(self, *sets):
        self._card_names = load_card_names(sets)

    def guess(self, crap_title):
        titles = process.extract(crap_title, self._card_names)
        print(titles, file=sys.stderr)
        return titles[0][0]
