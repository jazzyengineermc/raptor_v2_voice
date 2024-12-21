#!/usr/bin/python3
import vosk
import pyaudio
import json

WAKE_WORD = "raptor"
VOSK_MODEL = "/home/jreide/vosk-model-small-en-us-0.15"

def recognize_speech():
    model = vosk.Model(VOSK_MODEL)
    recognizer = vosk.KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    text_answer = None

    while text_answer is None:
        data = stream.read(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")
            text = text.lower()
            print(text)
            if WAKE_WORD in text:
                text = text.lower()
                text_answer = text.replace(WAKE_WORD, '')
                return text_answer

            if text_answer is not None:
                break


def wakeword_dictation():
    while True:
        user_input = recognize_speech()
        if user_input == "goodbye":
            print("Taa Taa For now.") # Play TTS wav
            break
        print(user_input)
        

print("Greetings and salutations, what is on your mind?") # Play TTS wav
wakeword_dictation()