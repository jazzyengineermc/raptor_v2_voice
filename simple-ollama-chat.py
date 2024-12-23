import os
from langchain.llms import Ollama

# Define system_message at the start of your script
SYSTEM_MESSAGE = "You are Raptor, a friendly AI assistant. KEEP RESPONSES VERY SHORT AND CONVERSATIONAL."
ollama = Ollama(base_url='http://localhost:11434', model='llava-phi3')  # Change model as needed

while True:

    # Recognize command
    query = input(">> ")
    print("Command: " + query)

    if query != "":
        # Send command to AI (e.g., llama2)
        text_ollama = ollama(f"{SYSTEM_MESSAGE} {query}")
        
        with open("output.txt", "w", encoding="utf-8") as output_file:
            sentences = text_ollama.split(". ")
            for sentence in sentences:
                output_file.write(sentence.strip() + "\n")
                print(sentence)

