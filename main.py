import cv2
import mediapipe as mp
import keyboard
import math
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path = "face_landmarker.task"

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def eye_ratio(points):
    top1 = points[1]
    top2 = points[2]
    bottom1 = points[4]
    bottom2 = points[5]
    left = points[0]
    right = points[3]

    height = distance(top1, bottom2) + distance(top2, bottom1)
    width = 2 * distance(left, right)
    return height / width


right_eye = [33, 160, 158, 133, 153, 144]
left_eye = [362, 385, 387, 263, 373, 380]
closed_threshold = 0.20
options = vision.FaceLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path=model_path),
    num_faces=1,
)

landmarker = vision.FaceLandmarker.create_from_options(options)
connections = vision.FaceLandmarksConnections.FACE_LANDMARKS_TESSELATION

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

if cap is None:
    print("couldn't open camera")
    landmarker.close()
    raise SystemExit

closed_frames = 0
frames_until_drowsy = 45

while True:
    ret, frame = cap.read()
    if not ret:
        print("failed to read from camera")
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = landmarker.detect(image)

    height, width = frame.shape[:2]
    if not result.face_landmarks:
        closed_frames = 0

    for face in result.face_landmarks:
        points = []
        for landmark in face:
            points.append((int(landmark.x * width), int(landmark.y * height)))

        right_ratio = eye_ratio([points[i] for i in right_eye])
        left_ratio = eye_ratio([points[i] for i in left_eye])
        eye_ratio_average = (right_ratio + left_ratio) / 2

        if eye_ratio_average <= closed_threshold:
            closed_frames += 1
            if closed_frames >= frames_until_drowsy:
                eye_status = "Drowsy"
            else:
                eye_status = "Eyes closed"
            status_color = (0, 0, 255)
        else:
            closed_frames = 0
            eye_status = "Eyes open"
            status_color = (0, 255, 0)
        print(eye_status, eye_ratio_average)

        for connection in connections:
            cv2.line(
                frame,
                points[connection.start],
                points[connection.end],
                (0, 255, 0),
                1,
            )

    cv2.imshow("face mesh", frame)
    cv2.waitKey(1)
    if keyboard.is_pressed("q"):
        break

cap.release()
landmarker.close()
cv2.destroyAllWindows()
