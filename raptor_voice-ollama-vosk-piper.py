#!/usr/bin/python3
import requests
import json
import vosk
import pyaudio
import requests
import subprocess as cmdLine
from datetime import datetime
from datetime import date
import todo as todo

# datetime object containing current date and time
now = datetime.now()
today = date.today()

# URL of the API endpoint
urlOllama = 'http://localhost:11434/api/chat'

urlPiper = "http://localhost:5000"
outputFilename = "output.wav"
SYSTEM_PROMPT = "You are Raptor, a friendly and supportive AI assistant. KEEP RESPONSES VERY SHORT AND CONVERSATIONAL."
WAKE_WORD = "raptor"
VOSK_MODEL = "/home/jreide/vosk-model-small-en-us-0.15"
 
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
            
            
def tts_piper(textToSpeak):
    payload = {'text': textToSpeak}

    r = requests.get(urlPiper,params=payload)

    with open(outputFilename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
            
    command = 'play '+ outputFilename 
    result = cmdLine.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    

def get_chat_response(query, chat_history):
    tts_piper("Processing a response.")
    # Data payload as JSON object with conversation history
    data = {
        "model": "llava-phi3",
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history + [{"role": "user", "content": query}]
    }

    # Convert data to JSON string
    json_data = json.dumps(data)

    # Define headers for the request
    headers = {'Content-Type': 'application/json'}

    # Send POST request with headers and body, enabling streaming
    response = requests.post(urlOllama, data=json_data, headers=headers, stream=True)

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
                    full_response += content
                       
                except json.JSONDecodeError as e:
                    print(f"JSON Decode Error: {e}")
        
        print("Full Response Body:")
        return full_response, chat_history[:10]  # Keep only the last 10 messages for context
    else:
        print(f"Error: {response.text}")
        return None, []
    

def new_chat():
    chat_history = []
    tts_piper("Mind Wiped, no chat history in buffer")
    

# Initialize chat history
chat_history = []

while True:
    user_input = recognize_speech()
    user_input = user_input.lower()
    user_input = user_input.strip()
    
    if user_input in ['exit', 'quit']:
        
        break
    
    if user_input in ['mindwipe', 'mind wipe', 'new chat']:
        
        new_chat()
        
        continue
    
    if user_input in ['bye', 'goodbye', 'good by', 'good bye']:
        
        tts_piper("ta ta for now")
        
        continue
    
    if user_input in ['what time is it', 'what day is it']:
        
        # 12 Hour format with am/pm
        dt_string = now.strftime("%I:%M %p")
        # Textual month, day and year	
        d2 = today.strftime("%B %d, %Y")
        tts_piper(f"The time is, {dt_string}, on {d2}")
        
        continue
    
    if user_input in ['what do you see']:
        
        # Get image from webcam and ask the LLM
        tts_piper("Nothing yet, I am not coded for that. Though I hear that is coming soon.")
        
        continue
    
    if 'to do list' in user_input:
        
        if 'add' in user_input:
            
            user_input = user_input.replace('add ', '')
            user_input = user_input.replace(' to my to do list', '')
            user_input = user_input.replace('\n', '')
            
            todo.add(s=str(user_input))
            tts_piper('added' + str(user_input) + 'to the to do list')
            user_input = ''
            
        elif 'delete' in user_input:
            
            user_input = user_input.replace('delete ', '')
            user_input = user_input.replace(' from my to do list', '')
            user_input = user_input.strip()
            
            todo.deL(no=user_input)
            tts_piper('removed number. ' + str(user_input) + ' from the todo list')
            user_input = ''
            
        elif 'read' in user_input:
             
            index_number = 1
            with open("todo.lst", "r") as file:
                for line in file:
                    # Process each line here
                    line = line.strip()
                    #newline = [index_number + ". " + line + "."]
                    print(f"{index_number}. {line}.")
                    tts_piper(f"{index_number}. {line}.")          
                    index_number = index_number+1
            user_input = ''
            
        else:
            
            tts_piper('I can add items to your list and I can read the list to you')
            tts_piper('Take note of the number as I read them as it is the number that I need to delete them')
            tts_piper('Until more input is received, I only see one item to do')
            tts_piper('Take over the world!')
            user_input = ''
            
        continue
                  
    response_text, chat_history = get_chat_response(user_input, chat_history)
    
    if response_text is not None:
        
        print(f"Bot: {response_text}")
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": response_text})
        #print(chat_history)
        tts_piper(response_text)
