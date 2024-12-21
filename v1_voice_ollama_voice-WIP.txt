import speech_recognition as sr
import pyttsx3
import requests
import json

# Set up global variables
SYSTEM_PROMPT = "You are Raptor, a friendly AI assistant. KEEP RESPONSES VERY SHORT AND CONVERSATIONAL."
WAKE_WORD = "raptor"
API_URL = "http://localhost:11434/v1/generate"  # URL for your Ollama instance
CHAT_HISTORY_SIZE = 10

# Initialize speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
mic = sr.Microphone()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty("rate", 350)
mbrola_voice_id = 'mbrola-en1'  # Change this if you are using mbrola-en1 specifically

# Set up the voice
if mbrola_voice_id in [voice.id for voice in voices]:
    engine.setProperty('voice', mbrola_voice_id)

# Initialize chat history as a list of dictionaries containing user and assistant messages
chat_history = []

def send_to_ollama(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "prompt": prompt,
        "system_prompt": SYSTEM_PROMPT,
        "max_new_tokens": 256,
        "temperature": 0.7
    })
    
    response = requests.post(API_URL, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()['results'][0]['text']
    else:
        print("Error communicating with Ollama:", response.text)
        return ""

def listen_for_wake_word():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        transcription = recognizer.recognize_google(audio, language='en-US')
        if WAKE_WORD.lower() in transcription.lower():
            print("Wake word detected:", transcription)
            return True
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    
    return False

def listen_and_talk():
    while True:
        if listen_for_wake_word():
            with mic as source:
                audio = recognizer.listen(source)
                try:
                    prompt_text = recognizer.recognize_google(audio, language='en-US')
                    print(f"User: {prompt_text}")

                    # Maintain chat history
                    chat_history.append({"role": "user", "content": prompt_text})

                    if len(chat_history) > CHAT_HISTORY_SIZE * 2:
                        chat_history.pop(0)

                    response = send_to_ollama(json.dumps(chat_history))

                    print(f"Raptor: {response}")
                    chat_history.append({"role": "assistant", "content": response})
                    
                    engine.say(response)
                    engine.runAndWait()

                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")

if __name__ == "__main__":
    listen_and_talk()