from  langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import vosk
import pyaudio
import json
from Espeak import *
import pyttsx3

WAKE_WORD = "raptor"
VOSK_MODEL = "/home/jreide/vosk-model-small-en-us-0.15"

bot_name = "Raptor"
model = OllamaLLM(model="phi3")

template = """
KEEP RESPONCES VERY SHORT AND CONVERSATIONAL. Answer the question below.
    
Here is the conversation history: {context}
    
Question: {question}
    
Answer:
"""
    
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Mouth --- default old voice
engine = pyttsx3.init()
engine.setProperty("rate", 350)
        
vmbrit = 'mb-en1 ' # Male Brittish Voice

voice = vmbrit
es = Espeak()

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


def chat_with_ollama():
    context = ""
    #print("Welcome to the ", bot_name, " chatbot! Type 'bye' to  quit.")
    while True:
        user_input = recognize_speech() # input("You: ") # Or Speech recognition input STT
        if user_input.lower() == "switch off":
            es.talk(voice, speech="tah tah for now")
            break
        
        result = chain.invoke({"context": context, "question": user_input})
        #print(bot_name, ": ", result) # Or TTS the result
        es.talk(voice, speech=result)
        context += f"\nUser: {user_input}\nAI: {result}"

        if len(context) > 10:
            context = context[-10:]
        
        
if __name__ == "__main__":
    es.talk(voice, speech="Greetings and salutations")
    chat_with_ollama()