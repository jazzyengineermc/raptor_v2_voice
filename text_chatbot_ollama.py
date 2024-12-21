from langchain.llms import Ollama

bot_name = "Raptor"
# Define system_message at the start of your script
SYSTEM_MESSAGE = "You are Raptor, a friendly AI assistant. KEEP RESPONSES VERY SHORT AND CONVERSATIONAL."
ollama = Ollama(base_url='http://localhost:11434', model='phi3')  # Change model as needed
chat_log_filename = "bot_chat.log"


def chat_ollama(query, SYSTEM_MESSAGE, conversation_history, bot_name):
    
    query = [{"role": "system", "content": SYSTEM_MESSAGE}] + conversation_history + [{"role": "user", "content": query}]

    streamed_completion = ollama(query)

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


conversation_history = []

while True:
    # Recognize command
    query = input(">> ")

    if query != "":
        conversation_history.append({"role": "user", "content": query})
        chatbot_responce = chat_ollama(query, SYSTEM_MESSAGE, conversation_history, bot_name)
        conversation_history.append({"role": "assistant", "content": chatbot_responce})
        
        prompt2 = chatbot_responce
        print(prompt2) # Or you can tts it, Example: es.talk(voice, speech=prompt2)  if you were using the Espeak.py module
        
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]