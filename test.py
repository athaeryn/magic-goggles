from __future__ import print_function

from glob import glob

from PIL import Image
import numpy as np

from vision import _get_cropped_card
from title_guesser import TitleGuesser, get_name_from_path


if __name__ == "__main__":
    guesser = TitleGuesser()

    cards = glob("./sample_imgs/*.jpg")

    for path in cards:
        card_name = get_name_from_path(path)

        img = Image.open(path)
        card = _get_cropped_card(np.array(img))

        best_guess = guesser.guess(card)[1]

        if card_name == best_guess:
            print(" ", card_name)
        else:
            print("X", card_name, "(guessed: " + best_guess + ")")
