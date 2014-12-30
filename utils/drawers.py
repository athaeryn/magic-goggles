import numpy as np
import cv2
import getters as get

def contours(src, dest, thickness=1, color=(0,0,255)):
    """
    Draw contours on an image
    """
    contours = get.contours(src)
    cv2.drawContours(dest, contours, -1, color, thickness)

def corners(src, dest, color=(0,255,0)):
    """
    Draw corners on an image
    """
    dest[get.corners(src)] = color
