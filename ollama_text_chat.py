from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM 

# Create an Ollama LLM
llm = OllamaLLM(model="phi3")

# Define system_message at the start of your script
SYSTEM_MESSAGE = "You are Raptor, a friendly AI assistant. KEEP RESPONSES VERY SHORT AND CONVERSATIONAL."
bot_name = "Raptor"
chat_log_filename = "bot_chat.log"

def chat_with_ollama(query, SYSTEM_MESSAGE, conversation_history, bot_name):
    query = [{"role": "system", "content": SYSTEM_MESSAGE}] + conversation_history + [{"role": "user", "content": query}]
    
    # Define a prompt template
    template = """
    {SYSTEM_MESSAGE}:
    {query}
    """

    prompt = PromptTemplate(
        input_variables=["query"],
        template=template,
    )

    # Create an LLM chain
    chain = LLMChain(llm=llm, prompt=prompt)

    # Run the chain
    result = chain.run(class_list=query)
    print(result)
    
    return result
    

conversation_history = []

while True:
    # Recognize command
    query = input(">> ") # Or STT, Example: query = listen_for_wakeword()

    if query != "":
        conversation_history.append({"role": "user", "content": query})
        chatbot_responce = chat_with_ollama(query, SYSTEM_MESSAGE, conversation_history, bot_name)
        conversation_history.append({"role": "assistant", "content": chatbot_responce})
        
        prompt2 = chatbot_responce
        print(prompt2) # Or you can tts it, Example: es.talk(voice, speech=prompt2)  if you were using the Espeak.py module
        
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]