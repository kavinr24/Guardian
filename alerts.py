from pathlib import Path
import pyttsx3
import winsound

YAWN_WARNING_MESSAGE = "Yawning detected. Please stay alert."
MICROSLEEP_WARNING_MESSAGE = "Sleeping detected. Please pull over."
ALERT_AUDIO_FILE = "C:\\Users\\kavinr\\Desktop\\Guardian\\alert.wav"


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


def play_audio_file(wait=False):
    flags = winsound.SND_FILENAME | winsound.SND_NODEFAULT
    flags |= winsound.SND_SYNC if wait else winsound.SND_ASYNC
    winsound.PlaySound(str(ALERT_AUDIO_FILE), flags)

if __name__ == "__main__":
    play_audio_file(wait=True)
    speak_yawn_warning()
    