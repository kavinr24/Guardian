import cv2
import mediapipe as mp
import keyboard
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path = "face_landmarker.task"
options = vision.FaceLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path=model_path),
    num_faces=1,
)

landmarker = vision.FaceLandmarker.create_from_options(options)
connections = vision.FaceLandmarksConnections.FACE_LANDMARKS_TESSELATION

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = landmarker.detect(image)

    height, width = frame.shape[:2]
    for face in result.face_landmarks:
        points = []
        for landmark in face:
            points.append((int(landmark.x * width), int(landmark.y * height)))

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
