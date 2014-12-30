import numpy as np
import cv2

def gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def edges(img):
    return cv2.Canny(img, 10, 200, apertureSize = 3)

def contours(img):
    _edges = edges(img)
    contours, hierarchy = cv2.findContours(_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def bounds(contours):
    cnt = contours[0]
    return cv2.boundingRect(cnt)

def corners(img):
    gray = np.float32(img)
    dist = cv2.cornerHarris(gray, 2, 3, 0.04)
    dist = cv2.dilate(dist, None)
    return dist > 0.1 * dist.max()
