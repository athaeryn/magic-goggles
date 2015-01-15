import cv2
import numpy as np
from math import atan2, degrees


def _compute_angle(line):
    (x1, y1, x2, y2) = line
    (dx, dy) = (x2 - x1, y2 - y1)
    rads = atan2(-dy, dx)
    return abs(degrees(rads))


def _compute_center(line):
    (x1, y1, x2, y2) = line
    return ((x1 + x2) / 2, (y1 + y2) / 2)


def _intersection(l1, l2):
    x1, y1, x2, y2 = l1
    x3, y3, x4, y4 = l2
    # http://en.wikipedia.org/wiki/Line-line_intersection#Given_two_points_on_each_line
    return (
        ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) /
        ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)),
        ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) /
        ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    )


def _crop(img, bounds):
    x1, y1, w, h = bounds
    x2 = x1 + w
    y2 = y1 + h
    return img[y1:y2, x1:x2]


def _get_cropped_card(img):
    gray = _gray(img)
    blurred = cv2.medianBlur(gray, 17)

    edges = cv2.dilate(cv2.Canny(blurred, 100, 100, 3), None)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 200, 300, 100)[0]

    vert = filter(lambda l: abs(_compute_angle(l) - 90) < 45, lines)
    hori = filter(lambda l: abs(_compute_angle(l) - 0) < 45, lines)

    edges = [
        sorted(hori, key=lambda l: _compute_center(l)[1])[0],   # top
        sorted(vert, key=lambda l: _compute_center(l)[0])[0],   # left
        sorted(hori, key=lambda l: _compute_center(l)[1])[-1],  # bottom
        sorted(vert, key=lambda l: _compute_center(l)[0])[-1]   # right
    ]

    rect = np.zeros((4, 2), dtype="float32")
    rect[0] = _intersection(edges[0], edges[1])  # top left
    rect[1] = _intersection(edges[0], edges[3])  # top right
    rect[2] = _intersection(edges[2], edges[3])  # bottom right
    rect[3] = _intersection(edges[2], edges[1])  # bottom left

    width = 480
    height = 680

    dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype="float32")

    matrix = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(img, matrix, (width, height))

    return warped, edges


def _get_contours(gray):
    blurred = cv2.medianBlur(gray, 3)
    edges = _edges(blurred)
    contours, hierarchy = cv2.findContours(
        edges,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )
    return contours


def _gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def _edges(img):
    return cv2.Canny(img, 10, 200, apertureSize=3)


def extract_title(img):
    card, edges = _get_cropped_card(img)

    for x1, y1, x2, y2 in edges:
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 4)

    top = card[0:card.shape[1] / 5, 0:card.shape[0]]

    gray = _gray(top)
    blurred = cv2.medianBlur(gray, 3)

    contours = _get_contours(blurred)
    outer, _, inner = sorted(contours, key=cv2.contourArea, reverse=True)[:3]

    box = cv2.boundingRect(outer)
    title = _crop(top, box)

    gray = _gray(title)
    _, thresh = cv2.threshold(gray, 128, 256, cv2.THRESH_BINARY)
    title = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    return title
