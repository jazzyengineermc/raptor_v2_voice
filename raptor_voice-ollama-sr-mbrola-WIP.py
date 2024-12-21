from  langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import pygame
import speech_recognition as sr
from Espeak import *
import pyttsx3

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

def listen_for_command():
    r = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("Listening for the wake word...")
            r.pause_threshold = 2
            audio = r.listen(source)
        
        try:
            command = r.recognize_google(audio, language='en')
            
            if "raptor" in command.lower():
                print(f"Wake word detected: {command}")
                #break
                command = command.replace('Raptor ', '')
                query = command
                return query
            
        except sr.UnknownValueError:
            continue
        except sr.RequestError as e:
            print(f"Could not request results; {e}")


def chat_with_ollama():
    context = ""
    #print("Welcome to the ", bot_name, " chatbot! Type 'bye' to  quit.")
    while True:
        user_input = listen_for_command() # input("You: ") # Or Speech recognition input STT
        if user_input.lower() == "bye":
            break
        
        result = chain.invoke({"context": context, "question": user_input})
        #print(bot_name, ": ", result) # Or TTS the result
        es.talk(voice, speech=result)
        context += f"\nUser: {user_input}\nAI: {result}"

        if len(context) > 10:
            context = context[-10:]
        
        
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    es.talk(voice, speech="Greeting and salutations")
    chat_with_ollama()