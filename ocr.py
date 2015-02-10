import Image
from pytesseract import image_to_string


def ocr(cvimage):
    """
    Run Tesseract on the title image in ./tmp.
    Returns the title as a string.
    """
    return image_to_string(Image.fromarray(cvimage)).replace("[", "")
