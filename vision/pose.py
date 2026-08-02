import cv2
import numpy as np

MODEL_POINTS = np.array(
    [
        (0.0, 0.0, 0.0),
        (0.0, -330.0, -65.0),
        (-225.0, 170.0, -135.0),
        (225.0, 170.0, -135.0),
        (-150.0, -150.0, -125.0),
        (150.0, -150.0, -125.0),
    ],
    dtype=np.float64,
)

POSE_LANDMARKS = (1, 152, 33, 263, 61, 291)


def _normalize_angle(angle):
    if angle > 90:
        angle -= 180
    elif angle < -90:
        angle += 180
    return angle


def calculate_head_pose(points, width, height):
    image_points = np.array(
        [points[index] for index in POSE_LANDMARKS],
        dtype=np.float64,
    )
    focal_length = width
    camera_matrix = np.array(
        [
            [focal_length, 0, width / 2],
            [0, focal_length, height / 2],
            [0, 0, 1],
        ],
        dtype=np.float64,
    )

    success, rotation_vector, _ = cv2.solvePnP(
        MODEL_POINTS,
        image_points,
        camera_matrix,
        np.zeros((4, 1)),
        flags=cv2.SOLVEPNP_ITERATIVE,
    )
    if not success:
        return None

    rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
    angles, _, _, _, _, _ = cv2.RQDecomp3x3(rotation_matrix)
    pitch = _normalize_angle(angles[0])
    yaw = _normalize_angle(angles[1])
    return pitch, yaw


def is_looking_away(pose, threshold=20):
    if pose is None:
        return False
    pitch, yaw = pose
    return abs(pitch) > threshold or abs(yaw) > threshold
