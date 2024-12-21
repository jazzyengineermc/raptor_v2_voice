#!/usr/bin/python3
from Espeak import *
import pyttsx3
from vosk import Model, KaldiRecognizer
import vosk
import pyaudio
import os
import json
from openai import OpenAI

# Set API configuration
client = OpenAI(base_url="http://jarvis.local:1234/v1", api_key="not-needed")
chat_log_filename = "raptor_chat.log"

# Ears
WAKE_WORD = "raptor"
VOSK_MODEL = "/home/jreide/vosk-model-small-en-us-0.15" # vosk-model-en-us-0.22

# Mouth --- default old voice
engine = pyttsx3.init()
engine.setProperty("rate", 350)       
vmbrit = 'mb-en1 ' # Male Brittish Voice
voice = vmbrit
es = Espeak()
# Example: es.talk(voice, speech="")


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


def chatgpt_streamed(user_input, system_message, conversation_history, bot_name):
    messages = [{"role": "system", "content": system_message}] + conversation_history + [{"role": "user", "content": user_input}]

    streamed_completion = client.chat.completions.create(
        model="llava-llama-3-8b-v1_1",
        messages=messages,
        stream=True,
        temperature=1
    )

    full_responce = ""
    line_buffer = ""

    with open(chat_log_filename, "a") as log_file:
        for chunk in streamed_completion:
            delta_content = chunk.choices[0].delta.content

            if delta_content is not None:
                line_buffer += delta_content

                if '\n' in line_buffer:
                    lines = line_buffer.split('\n')
                    for line in lines[:-1]:
                        full_responce += line + '\n'
                        log_file.write(f"{bot_name}: {line}\n")
                    line_buffer = lines[-1]

        if line_buffer:
            full_responce += line_buffer
            log_file.write(f"{bot_name}: {line_buffer}\n")

    return full_responce


def user_chatbot_conversation():
    conversation_history = []
    system_message = "You are Raptor, an advanced artificial intelligence modeled after Jarvis from the Iron Man movies. KEEP RESPONCES VERY SHORT AND CONVERSATIONAL."
    while True:
        # Mic to speech reconizer, return user_input
        # user_input = input(">> ")
        user_input = recognize_speech()
        if user_input == "goodbye":
            es.talk(voice, speech="Taa Taa For now.") # Play TTS wav
            break
        # print(user_input)
        conversation_history.append({"role": "user", "content": user_input})
        chatbot_responce = chatgpt_streamed(user_input, system_message, conversation_history, "Jarvis")
        conversation_history.append({"role": "assistant", "content": chatbot_responce})

        prompt2 = chatbot_responce
        es.talk(voice, speech=prompt2) # Play TTS wav

        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]


es.talk(voice, speech="Greetings and salutations, what is on your mind?") # Play TTS wav
user_chatbot_conversation()

