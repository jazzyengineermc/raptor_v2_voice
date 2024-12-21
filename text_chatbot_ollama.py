from  langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

bot_name = "Raptor"
model = OllamaLLM(model="phi3")

template = """
You are Raptor, a friendly AI assistant. KEEP RESPONCES VERY SHORT AND CONVERSATIONAL. Answer the question below.
    
Here is the conversation history: {context}
    
Question: {question}
    
Answer:
"""
    
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def chat_with_ollama():
    context = ""
    print("Welcome to the ", bot_name, " chatbot! Type 'bye' to  quit.")
    while True:
        user_input = input("You: ") # Or Speech recognition input STT
        if user_input.lower() == "bye":
            break
        
        result = chain.invoke({"context": context, "question": user_input})
        print(bot_name, ": ", result) # Or TTS the result
        context += f"\nUser: {user_input}\nAI: {result}"

        if len(context) > 10:
            context = context[-10:]
        
        
if __name__ == "__main__":
    chat_with_ollama()