import os
import pygame
import speech_recognition as sr


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



while True:
    pygame.init()
    pygame.mixer.init()

    # Recognize command
    query = listen_for_command()
    
    print("Command: " + query)

