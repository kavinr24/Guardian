import os
import subprocess
from pathlib import Path

import pyttsx3

if os.name == "nt":
    import winsound


YAWN_WARNING_MESSAGE = "Yawning detected. Please stay alert."
MICROSLEEP_WARNING_MESSAGE = "Sleeping detected. Please pull over."
DISTRACTION_WARNING_MESSAGE = "Please keep your eyes on the road."
ALERT_AUDIO_FILE = Path(__file__).resolve().parent / "alert.wav"


def speak_message(message, rate=175, volume=1.0):
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)
    engine.say(message)
    engine.runAndWait()
    engine.stop()


def speak_yawn_warning():
    speak_message(YAWN_WARNING_MESSAGE)


def speak_microsleep_warning():
    speak_message(MICROSLEEP_WARNING_MESSAGE)


def speak_distraction_warning():
    speak_message(DISTRACTION_WARNING_MESSAGE)


def play_audio_file(wait=False):
    audio_path = str(ALERT_AUDIO_FILE)

    if os.name == "nt":
        flags = winsound.SND_FILENAME | winsound.SND_NODEFAULT
        flags |= winsound.SND_SYNC if wait else winsound.SND_ASYNC
        winsound.PlaySound(audio_path, flags)
    else:
        process = subprocess.Popen(
            ["aplay", audio_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if wait:
            process.wait()


if __name__ == "__main__":
    play_audio_file(wait=True)
    speak_yawn_warning()
