import requests
import json
import vosk
import pyaudio
import requests
import subprocess as cmdLine

# URL of the API endpoint
url = 'http://localhost:11434/api/chat'

urlPiper = "http://localhost:5000"
outputFilename = "output.wav"
SYSTEM_PROMPT = "You are Raptor, a friendly AI assistant. KEEP RESPONSES VERY SHORT AND CONVERSATIONAL."
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
    # Data payload as JSON object with conversation history
    data = {
        "model": "llava-phi3",
        "system": SYSTEM_PROMPT,
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
    user_input = recognize_speech() # input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        break
    
    response_text, chat_history = get_chat_response(user_input, chat_history)
    if response_text is not None:
        print(f"Bot: {response_text}")
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": response_text})
        #print(chat_history)
        tts_piper(response_text)
