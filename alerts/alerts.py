import json
import os
import subprocess
import threading
import urllib.request
from pathlib import Path

import pyttsx3
from dotenv import load_dotenv

if os.name == "nt":
    import winsound


YAWN_WARNING_MESSAGE = "Yawning detected. Please stay alert."
MICROSLEEP_WARNING_MESSAGE = "Sleeping detected. Please pull over."
DISTRACTION_WARNING_MESSAGE = "Please keep your eyes on the road."
ALERT_AUDIO_FILE = Path(__file__).resolve().parent / "alert.wav"
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_FILE)
DISCORD_WEBHOOK_URL = os.getenv("DC_WEBHOOK", "")
DISCORD_SLEEP_MESSAGE = "@everyone GUARDIAN USER IS SLEEPING WHILE DRIVING, PLEASE LOCATE AND HELP THE DRIVER."


def send_discord_webhook():
    if not DISCORD_WEBHOOK_URL:
        print("no webhook url found in env")
        return

    def post_webhook():
        payload = json.dumps({"content": DISCORD_SLEEP_MESSAGE}).encode("utf-8")
        request = urllib.request.Request(
            DISCORD_WEBHOOK_URL,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Guardian/1.0",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                print(f"webhook sent: HTTP {response.status}")
        except Exception as error:
            print(f"webhook failed {error}")

    threading.Thread(target=post_webhook, daemon=True).start()


def speak_message(message, rate=175, volume=1.0):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", rate)
        engine.setProperty("volume", volume)
        engine.say(message)
        engine.runAndWait()
        engine.stop()
    except Exception as error:
        print(f"TTS unavailable: {error}")


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
