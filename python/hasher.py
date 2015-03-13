import cv2
import numpy as np
import imagehash
from PIL import Image

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
