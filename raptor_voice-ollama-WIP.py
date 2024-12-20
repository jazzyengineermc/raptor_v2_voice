from gtts import gTTS
import os
import pygame
from langchain.llms import Ollama
import speech_recognition as sr

# Safely deleted all files if there was an error running last time
for mp3_file in os.listdir("mp3_files"):
    if mp3_file.endswith(".mp3"):
        mp3_file_path = os.path.join("mp3_files", mp3_file)
        os.remove(mp3_file_path)

def play(file_path):
    # Play MP3s with the pygame mixer
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(f"Error while playing {file_path}: {e}")

    finally:
        pygame.mixer.music.stop()

def generate_mp3(output_folder):
    # For every line in output, generate an MP3 file
    with open("output.txt", "r", encoding="utf-8") as input_file:
        for line_number, line in enumerate(input_file):
            line = line.strip()
            
            if line == "":
                continue

            voice = "en-US-EricNeural"
            mp3_file_path = os.path.join(output_folder, f"output_{line_number+10}.mp3")
            command = f'edge-tts --voice "{voice}" --text "{line}" --write-media "{mp3_file_path}"'
            os.system(command)
            print(f"Generated MP3 for line {line_number}: {mp3_file_path}")

def speak():
    output_folder = "mp3_files"
    
    # Generate MP3 file for TTS
    generate_mp3(output_folder)

    try:
        # Play every MP3 file
        mp3_files = [file for file in os.listdir(output_folder) if file.endswith(".mp3")]
        
        mp3_files.sort()
        print(mp3_files)
        
        for mp3_file in mp3_files:
            mp3_file_path = os.path.join(output_folder, mp3_file)
            play(mp3_file_path)

        pygame.mixer.quit()

    except Exception as e:
        print(f"Error while playing: {e}")

    finally:
        # Delete all played MP3 files
        for mp3_file in os.listdir(output_folder):
            if mp3_file.endswith(".mp3"):
                mp3_file_path = os.path.join(output_folder, mp3_file)
                os.remove(mp3_file_path)

def take_command():
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

# Now that the wake word is detected, capture and process the actual command

ollama = Ollama(base_url='http://localhost:11434', model='phi3')  # Change model as needed

while True:
    pygame.init()
    pygame.mixer.init()

    # Recognize command
    query = take_command()
    print("Command: " + query)

    if query != "":
        # Send command to AI (e.g., llama2)
        text_ollama = ollama(query)
        
        with open("output.txt", "w", encoding="utf-8") as output_file:
            sentences = text_ollama.split(". ")
            for sentence in sentences:
                output_file.write(sentence.strip() + "\n")

    # Read out the response from the AI
    speak()
