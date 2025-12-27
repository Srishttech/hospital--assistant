import queue
import json
import sounddevice as sd
import os
from vosk import Model, KaldiRecognizer
from gtts import gTTS

# ---------------------------
# Audio Queue
# ---------------------------
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))


# ---------------------------
# Speech to Text (STT)
# ---------------------------
# def listen(timeout=15, lang="en"):
#     """
#     lang = "en" or "hi"
#     """
#     BASE_DIR = os.path.dirname(__file__)

#     # ✅ Choose correct model
#     if lang == "hi":
#         model_path = os.path.join(BASE_DIR, "models", "vosk-model-small-hi-0.22")
#     else:
#         model_path = os.path.join(BASE_DIR, "models", "vosk-model-small-en-us-0.15")

#     if not os.path.exists(model_path):
#         raise FileNotFoundError(f"Vosk model not found at: {model_path}")

#     # ✅ Clear old audio (VERY IMPORTANT)
#     while not q.empty():
#         q.get()

#     model = Model(model_path)
#     rec = KaldiRecognizer(model, 16000)

#     print(f"🎤 Listening ({lang.upper()})... Speak now")

#     with sd.RawInputStream(
#         samplerate=16000,
#         blocksize=8000,
#         dtype="int16",
#         channels=1,
#         callback=callback,
#     ):
#         sd.sleep(timeout * 1000)

#         while True:
#             data = q.get()
#             if rec.AcceptWaveform(data):
#                 result = json.loads(rec.Result())
#                 text = result.get("text", "")
#                 return text.strip()
def listen(timeout=15, lang="en"):
    BASE_DIR = os.path.dirname(__file__)

    if lang == "hi":
        model_path = os.path.join(BASE_DIR, "models", "vosk-model-small-hi-0.22")
    else:
        model_path = os.path.join(BASE_DIR, "models", "vosk-model-small-en-us-0.15")

    while not q.empty():
        q.get()

    model = Model(model_path)
    rec = KaldiRecognizer(model, 16000)

    print(f"🎤 Listening ({lang})...")

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        sd.sleep(timeout * 1000)

        final_text = ""

        while not q.empty():
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                final_text += " " + result.get("text", "")

        # 🔥 Get final partial result
        partial = json.loads(rec.FinalResult()).get("text", "")
        final_text += " " + partial

        return final_text.strip()


# ---------------------------
# Text to Speech (TTS)
# ---------------------------
def speak(text, lang="en"):
    """
    lang = "en" or "hi"
    """
    print("🔊 Assistant:", text)

    tts = gTTS(text=text, lang=lang)
    filename = f"response_{lang}.mp3"
    tts.save(filename)

    # Auto-play
    if os.name == "nt":  # Windows
        os.system(f"start {filename}")
    elif os.uname().sysname == "Darwin":  # macOS
        os.system(f"afplay {filename}")
    else:  # Linux
        os.system(f"xdg-open {filename}")


# ---------------------------
# Test Run (Optional)
# ---------------------------
if __name__ == "__main__":
    speak("Hello, please speak in English", "en")
    text = listen(lang="en")
    print("You said:", text)

    speak("अब हिंदी में बोलिए", "hi")
    text = listen(lang="hi")
    print("आपने कहा:", text)
