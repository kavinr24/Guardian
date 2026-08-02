import math

MOUTH_TOP = 13
MOUTH_BOTTOM = 14
MOUTH_LEFT = 61
MOUTH_RIGHT = 291

def _distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def calculate_mar(points):
    opening = _distance(points[MOUTH_TOP], points[MOUTH_BOTTOM])
    width = _distance(points[MOUTH_LEFT], points[MOUTH_RIGHT])
    return opening / width
