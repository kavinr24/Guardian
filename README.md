# Guardian
Real-time driver safety monitoring powered by computer vision.

## Features
 - **Facial Landmark Tracking:** Uses OpenCV and MediaPipe to track eyes, mouth, and head pose in real time.
 - **FPS-Independent Timers:** Uses time diffs (`time.time()`) instead of frame counts so thresholds stay accurate on low end hardware like the Raspberry Pi 5. 
 - **Sleep & Yawn Detection:** Triggers warnings for long eye closure, microsleeps, and yawning.
 - **Distraction Monitoring:** Flags when the driver looks away from the road for too long.
 - **Flicker Filtering:** Smooths out detections so that quick blinks don't reset the sleep counter.
 - **Cross-Platform Audio:** Uses `aplay` on Linux/RPi and `winsound` on Windows so audio playback never lags the detection loop.
 - **Emergency Discord Webhook:** Pings a Discord channel with `@everyone` if the driver remains asleep for over 10 seconds.
 - **Headless Mode Support:** Option to run without rendering GUI windows (`cv2.imshow`) to conserve hardware resources.

## Tech Stack
 - **Language:** Python 3.14
 - **Computer Vision:** OpenCV, MediaPipe
 - **Audio & TTS:** pyttsx3, ALSA (`aplay` - Linux) / `winsound` (Windows)
 - **Networking:** `urllib` / `requests` (Discord Webhooks)

 ## Usage
 Clone or download the repo and cd into it:
    `git clone https://github.com/kavinr/Guardian`  
    `cd Guardian`  
    
Install required libraries: 
    `pip install -r requirements.txt`  

Run the main detection loop:  
    `python main.py`  
Headless mode (no video display)  
    `python main.py --headless`  

## Configuration

All detection values are arguments in the `SafetyDetector` class in `vision/detector.py`. Adjust them directly in that file:

```python
detector = SafetyDetector(
    closed_threshold=0.20,
    drowsy_duration_seconds=1.5,
    mouth_threshold=0.60,
    yawn_duration_seconds=1.0,
    pose_threshold=20,
    distraction_duration_seconds=1.5,
    eye_open_grace_seconds=0.25,
    awake_reset_seconds=3.0,
    emergency_sleep_duration_seconds=10.0,
)
```

| Parameter | Default | What it controls |
|---|---|---|
| `closed_threshold` | `0.20` | Eye Aspect Ratio (EAR) at or below which the eyes count as closed. Lower = harder to trigger. |
| `drowsy_duration_seconds` | `1.5` | Seconds the eyes must stay closed before a drowsiness/microsleep alert gets triggered. |
| `mouth_threshold` | `0.60` | Mouth Aspect Ratio (MAR) above which the mouth counts as open. |
| `yawn_duration_seconds` | `1.0` | Seconds the mouth must stay open before a yawn warning triggers. |
| `pose_threshold` | `20` | Head pitch or yaw threshold which you count as looking away from the road. |
| `distraction_duration_seconds` | `1.5` | Seconds you must look away before a distraction warning triggers. |
| `eye_open_grace_seconds` | `0.25` | Blink buffer: if "eyes open" reads shorter than this then the sleep timer doesn't get reset. |
| `awake_reset_seconds` | `3.0` | Seconds you must stay awake before the Discord emergency alert can be sent again. |
| `emergency_sleep_duration_seconds` | `10.0` | Continuous sleep time before the Discord `@everyone` webhook is sent. |

Other settings:

- **Discord webhook:** set `DC_WEBHOOK` in `.env` (used for the emergency sleep alert).
- **Spoken warning text:** edit `YAWN_WARNING_MESSAGE`, `MICROSLEEP_WARNING_MESSAGE`, and `DISTRACTION_WARNING_MESSAGE` in `alerts/alerts.py`.
- **Alert sound:** replace `alerts/alert.wav` with your own audio.
- **Camera:** `main.py` opens camera index `0`, change `cv2.VideoCapture(0)` for a different device.



