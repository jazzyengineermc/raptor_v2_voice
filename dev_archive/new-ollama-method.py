import requests
import json

# URL of the API endpoint
url = 'http://localhost:11434/api/chat'

def get_chat_response(query, chat_history):
    # Data payload as JSON object with conversation history
    data = {
        "model": "llava-phi3",
        "messages": chat_history + [{"role": "user", "content": query}]
    }

    # Convert data to JSON string
    json_data = json.dumps(data)

    # Define headers for the request
    headers = {'Content-Type': 'application/json'}

    # Send POST request with headers and body, enabling streaming
    response = requests.post(url, data=json_data, headers=headers, stream=True)

    # Print response status code
    print(f"Response Status Code: {response.status_code}")

    if response.status_code == 200:
        full_response = ""

        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                try:
                    json_chunk = json.loads(chunk.decode('utf-8'))
                    content = json_chunk['message']['content']
                    # Append the bot's message to chat history
                    chat_history.append({"role": "assistant", "content": content})
                    full_response += content
                except json.JSONDecodeError as e:
                    print(f"JSON Decode Error: {e}")
        
        print("Full Response Body:")
        return full_response, chat_history[:10]  # Keep only the last 10 messages for context
    else:
        print(f"Error: {response.text}")
        return None, []

# Initialize chat history
chat_history = []

while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        break

    response_text, chat_history = get_chat_response(user_input, chat_history)
    if response_text is not None:
        print(f"Bot: {response_text}")
