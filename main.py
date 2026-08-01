import cv2
import keyboard
from vision.detector import CONNECTIONS, SafetyDetector

def main():
    detector = SafetyDetector()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("couldn't open camera")
        detector.close()
        raise SystemExit

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("failed to read from camera")
                break

            detection = detector.process(frame)

            for connection in CONNECTIONS:
                if detection.points:
                    cv2.line(frame,detection.points[connection.start],detection.points[connection.end],(0, 255, 0),1,)

            cv2.putText(frame,detection.eye_status,(20, 40),cv2.FONT_HERSHEY_SIMPLEX,1,detection.status_color,2,)
            cv2.putText(frame,detection.yawn_status,(20, 80),cv2.FONT_HERSHEY_SIMPLEX,1,detection.yawn_color,2,)

            if detection.eye_ratio is not None:
                print(detection.eye_status, detection.eye_ratio, detection.yawn_status, detection.mouth_ratio)

            cv2.imshow("face mesh", frame)
            cv2.waitKey(1)

            if keyboard.is_pressed("q"):
                break
    finally:
        cap.release()
        detector.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
