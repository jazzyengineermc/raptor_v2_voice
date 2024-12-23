import json
from datetime import datetime
import requests

# Configuration section (top of the script)
API_URL = "http://localhost:11434/v1/chat/completions"  # Replace with your actual API endpoint if necessary.
TOKEN = "your_api_token_here"                          # Replace this with your token or use an environment variable.
MODEL_NAME = "llava-phi3"                       # The model to use for generating chat completions.
CHATBOT_NAME = "Raptor"                          # Name of the chatbot.
SYSTEM_MESSAGE = f"You are {CHATBOT_NAME}. a friendly AI assistant. KEEP RESPONCES VERY SHORT AND CONVERSATIONAL."  # System message that sets up the chatbot's role.

# Initialize conversation history
conversation_history = []

def get_conversation_context():
    """Returns the last 10 messages in the conversation."""
    return [{"role": "system", "content": SYSTEM_MESSAGE}] + conversation_history[-9:]

def send_message(user_input):
    """Send a message to the Ollama API and receive a response."""
    context = get_conversation_context()
    
    # Prepare request payload
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": role, "content": content} for role, content in context]
    }
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print(f"Error: {response.status_code}")
        return None

def record_conversation(role, content):
    """Records the conversation to history."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = {"role": role, "content": content, "timestamp": timestamp}
    conversation_history.append(message)

# Main interaction loop
def main():
    print(f"Welcome! I'm {CHATBOT_NAME}. How can I assist you today?")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        record_conversation("user", user_input)
        
        bot_response = send_message(user_input)
        if bot_response is not None:
            print(f"{CHATBOT_NAME}: {bot_response}")
            
            # Record the chatbot's response
            record_conversation("assistant", bot_response)

if __name__ == "__main__":
    main()
