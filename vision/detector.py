from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from .ear import LEFT_EYE, RIGHT_EYE, calculate_ear
from .mar import calculate_mar
from .pose import calculate_head_pose, is_looking_away

CONNECTIONS = vision.FaceLandmarksConnections.FACE_LANDMARKS_TESSELATION

@dataclass
class SafetyResult:
    eye_status: str
    yawn_status: str
    eye_ratio: Optional[float]
    mouth_ratio: Optional[float]
    points: list
    status_color: tuple
    yawn_color: tuple
    distraction_status: str
    distraction_color: tuple
    pitch: Optional[float]
    yaw: Optional[float]


class SafetyDetector:
    def __init__(
        self,
        closed_threshold=0.20,
        frames_until_drowsy=45,
        mouth_threshold=0.60,
        frames_until_yawn=30,
        pose_threshold=20,
        frames_until_distraction=45,
    ):
        model_path = Path(__file__).resolve().parent / "face_landmarker.task"
        options = vision.FaceLandmarkerOptions(
            base_options=python.BaseOptions(model_asset_path=str(model_path)),
            num_faces=1,
        )
        self.landmarker = vision.FaceLandmarker.create_from_options(options)
        self.closed_threshold = closed_threshold
        self.frames_until_drowsy = frames_until_drowsy
        self.mouth_threshold = mouth_threshold
        self.frames_until_yawn = frames_until_yawn
        self.closed_frames = 0
        self.yawn_frames = 0
        self.distraction_frames = 0
        self.pose_threshold = pose_threshold
        self.frames_until_distraction = frames_until_distraction

    def process(self, frame):
        height, width = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = self.landmarker.detect(image)

        if not result.face_landmarks:
            self.closed_frames = 0
            self.yawn_frames = 0
            self.distraction_frames = 0
            return SafetyResult(
                eye_status="No face",
                yawn_status="No yawn",
                eye_ratio=None,
                mouth_ratio=None,
                points=[],
                status_color=(255, 255, 255),
                yawn_color=(0, 255, 0),
                distraction_status="No face",
                distraction_color=(255, 255, 255),
                pitch=None,
                yaw=None,
            )

        face = result.face_landmarks[0]
        points = [
            (int(landmark.x * width), int(landmark.y * height))
            for landmark in face
        ]

        right_ear = calculate_ear([points[index] for index in RIGHT_EYE])
        left_ear = calculate_ear([points[index] for index in LEFT_EYE])
        average_ear = (right_ear + left_ear) / 2

        if average_ear <= self.closed_threshold:
            self.closed_frames += 1
            eye_status = (
                "Drowsy"
                if self.closed_frames >= self.frames_until_drowsy
                else "Eyes closed"
            )
            status_color = (0, 0, 255)
        else:
            self.closed_frames = 0
            eye_status = "Eyes open"
            status_color = (0, 255, 0)

        pose = calculate_head_pose(points, width, height)
        pitch = pose[0] if pose is not None else None
        yaw = pose[1] if pose is not None else None
        if is_looking_away(pose, self.pose_threshold):
            self.distraction_frames += 1
            if self.distraction_frames >= self.frames_until_distraction:
                distraction_status = "Distraction warning"
                distraction_color = (0, 0, 255)
            else:
                distraction_status = "Checking pose"
                distraction_color = (0, 255, 255)
        else:
            self.distraction_frames = 0
            distraction_status = "Pose normal"
            distraction_color = (0, 255, 0)

        current_mar = calculate_mar(points)
        if current_mar > self.mouth_threshold:
            self.yawn_frames += 1
            if self.yawn_frames >= self.frames_until_yawn:
                yawn_status = "Yawn warning"
                yawn_color = (0, 0, 255)
            else:
                yawn_status = "No yawn"
                yawn_color = (0, 255, 0)
        else:
            self.yawn_frames = 0
            yawn_status = "No yawn"
            yawn_color = (0, 255, 0)

        return SafetyResult(
            eye_status=eye_status,
            yawn_status=yawn_status,
            eye_ratio=average_ear,
            mouth_ratio=current_mar,
            points=points,
            status_color=status_color,
            yawn_color=yawn_color,
            distraction_status=distraction_status,
            distraction_color=distraction_color,
            pitch=pitch,
            yaw=yaw,
        )

    def close(self):
        self.landmarker.close()
