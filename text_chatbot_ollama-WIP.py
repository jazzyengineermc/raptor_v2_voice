import os
import json
from openai import OpenAI

# Set API configuration
client = OpenAI(base_url="http://jarvis.local:1234/v1", api_key="not-needed")
chat_log_filename = "raptor_chat.log"


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
        user_input = input(">> ")
        # user_input = recognize_speech()
        if user_input == "goodbye":
            print("Taa Taa For now.") # Play TTS wav
            break
        # print(user_input)
        conversation_history.append({"role": "user", "content": user_input})
        chatbot_responce = chatgpt_streamed(user_input, system_message, conversation_history, "Jarvis")
        conversation_history.append({"role": "assistant", "content": chatbot_responce})

        prompt2 = chatbot_responce
        print(prompt2) # Play TTS wav

        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]


print("Greetings and salutations, what is on your mind?") # Play TTS wav
user_chatbot_conversation()

