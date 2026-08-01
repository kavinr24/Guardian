import math

RIGHT_EYE = [33, 160, 158, 133, 153, 144]
LEFT_EYE = [362, 385, 387, 263, 373, 380]

def _distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def calculate_ear(points):
    top1 = points[1]
    top2 = points[2]
    bottom1 = points[4]
    bottom2 = points[5]
    left = points[0]
    right = points[3]

    height = _distance(top1, bottom2) + _distance(top2, bottom1)
    width = 2 * _distance(left, right)
    return height / width
