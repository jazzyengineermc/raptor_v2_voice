import requests

# Define your base API URL for Ollama.
BASE_URL = "http://localhost:11434"
BOT_TYPE = "You are Raptor, a friendly AI assistant. KEEP RESPONCES VERY SHORT AND CONVERSATIONAL."

class ChatBot:
    def __init__(self, model="phi3", max_history=10, max_tokens=3000, bot_type=BOT_TYPE):
        self.history = []
        self.model = model
        self.max_history = max_history
        self.max_tokens = max_tokens
        self.bot_type = bot_type
    
    def get_response(self, prompt):
        url = f"{BASE_URL}/api/generate"
        
        headers = {
            'Content-Type': 'application/json',
        }
        
        # Prepare the history and current prompt for the request
        conversation_parts = ["System Message: " + self.bot_type]
        recent_history = "\n".join(self.history[-self.max_history:])
        if recent_history:
            conversation_parts.append(recent_history)
        conversation_parts.append(f"You: {prompt}")
        
        conversation = "\n".join(conversation_parts)

        data = {
            'prompt': conversation,
            'max_tokens': self.max_tokens,  # Adjust based on model limitations
            'temperature': 0.7,             # Control randomness of the response (lower is deterministic)
            'top_p': 0.95,                  # Nucleus sampling parameter to control diversity
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                text_response = response.json().get('text', '')
                self.history.append(f"You: {prompt}\nBot: {text_response}")
                return text_response
            else:
                self.history.append(f"You: {prompt}\nError: {response.status_code} - {response.text}")
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            self.history.append(f"You: {prompt}\nError: {str(e)}")
            return str(e)

    def main(self):
        while True:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            response = self.get_response(user_input)
            print(f"Bot: {response}")
    
if __name__ == "__main__":
    bot = ChatBot(model="phi3", max_history=10, max_tokens=3000, bot_type=BOT_TYPE)
    bot.main()
