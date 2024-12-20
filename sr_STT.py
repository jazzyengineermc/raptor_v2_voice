import speech_recognition as sr

# Initialize recognizer
r = sr.Recognizer()

def listen_for_wake_word():
    with sr.Microphone() as source:
        print("Waiting for wake word 'Charlie'...")
        while True:
            audio_data = r.listen(source, timeout=None)
            try:
                text = r.recognize_google(audio_data)
                if "Charlie" in text.lower():  # Detect the wake word
                    print(f"Wake word detected: {text}")
                    return
            except sr.UnknownValueError:
                pass

def on_wake_word_detected():
    print("Wake word detected! Listening for full sentence...")

def on_audio_received(r, audio):
    try:
        text = r.recognize_google(audio)
        if text.lower().startswith('charlie '):  # Ensure the wake word is at the beginning
            print(f"Wake word detected: {text}")
            global listening_for_sentence
            listening_for_sentence = True
        elif listening_for_sentence:
            print(f"Recognized speech: {text}")
    except sr.UnknownValueError:
        pass

def start_listening():
    r.listen_in_background(sr.Microphone(), on_audio_received)
    while True:
        listen_for_wake_word()

# Global flag to control sentence recognition
listening_for_sentence = False

if __name__ == '__main__':
    try:
        start_listening()
    except KeyboardInterrupt:
        print("Stopping...")
