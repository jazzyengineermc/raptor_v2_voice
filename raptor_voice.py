import os
from pydub import AudioSegment, playback
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import requests

# Configuration variables
WAKE_WORD = "raptor"
OLLAMA_URL = "http://localhost:8080"
LANGUAGE_CODE = "en"  # Language code for Vosk and TTS models (e.g., 'en' for English)
TTS_MODEL_NAME = "rafalosa/tts_difussor_male"  # Example: Use a male British voice

# Load vosk model
MODEL_PATH = "./vosk-model-en-us-0.22"
model = Model(MODEL_PATH)

def transcribe_audio(audio_data):
    rec = KaldiRecognizer(model, 16000)
    
    wav.write('temp_audio.wav', 16000, np.array(audio_data))
    with open('temp_audio.wav', 'rb') as f:
        while True:
            data = f.read(4096)
            if len(data) == 0: break
            if rec.AcceptWaveform(data):
                result = rec.Result()
                return result.split(":")[1][:-2]  # Extract the transcribed text

def send_to_ollama(conversation_history, prompt_text, ollama_url=OLLAMA_URL):
    headers = {'Content-Type': 'application/json'}
    
    conversation_with_prompt = "\n".join(conversation_history[-10:])  # Limit to last 10 messages
    if prompt_text:
        conversation_with_prompt += f"\nUser: {prompt_text}"
    
    response = requests.post(ollama_url + "/api/generate", json={'context': conversation_with_prompt}, headers=headers)
    
    if response.status_code == 200:
        return response.json()['response']
    else:
        print(f"Error: {response.status_code}")
        return ""

def generate_audio_response(text, model_name=TTS_MODEL_NAME):
    from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech
    processor = SpeechT5Processor.from_pretrained(model_name)
    model = SpeechT5ForTextToSpeech.from_pretrained(model_name)

    inputs = processor(text=text, return_tensors="pt")
    speech = model.generate(**inputs).waveform[0].numpy()

    # Convert to AudioSegment
    audio_segment = AudioSegment(speech.tobytes(), frame_rate=16000, sample_width=2, channels=1)
    
    return audio_segment

def listen_for_wake_word(wake_word=WAKE_WORD):
    import sounddevice as sd
    
    CHUNK_SIZE = 4096
    RATE = 16000
    
    frames = []
    streaming = False

    def callback(indata, frames, time, status):
        if not streaming:
            text = transcribe_audio(indata)
            print(f"Transcribed: {text}")
            
            if wake_word in text:
                print(f"Detected wake word: '{wake_word}'")
                global streaming
                streaming = True

    stream = sd.InputStream(samplerate=RATE, blocksize=CHUNK_SIZE, channels=1, callback=callback)
    
    print(f"Listening for wake word '{wake_word}'...")
    
    try:
        with stream:
            while not streaming:
                pass  # Keep listening until the wake word is detected
    finally:
        return 'temp_audio.wav'

def play_audio_file(file_path):
    sound = AudioSegment.from_wav(file_path)
    playback.play(sound)

# Main function
def main():
    conversation_history = []
    
    while True:
        # Listen for the wake word and get audio data
        audio_data_file = listen_for_wake_word()
        
        if not audio_data_file:
            continue
        
        # Transcribe the audio file
        transcribed_text = transcribe_audio(AudioSegment.from_wav(audio_data_file).get_array_of_samples())
        print(f"Transcribed Text: {transcribed_text}")

        # Add the user's message to the chat history
        if transcribed_text.strip():
            conversation_history.append(f"User: {transcribed_text}")

        # Send text to Ollama server and get response
        ollama_response_text = send_to_ollama(conversation_history, transcribed_text)
        print(f"Ollama Response: {ollama_response_text}")
        
        if ollama_response_text.strip():
            conversation_history.append(f"Assistant: {ollama_response_text}")

        # Generate audio from the response
        generated_audio_segment = generate_audio_response(ollama_response_text)

        # Save or play the generated audio (Optional: Play it directly using pydub's play method)
        generated_audio_segment.export("generated_output.wav", format="wav")
        print(f"Generated audio saved to 'generated_output.wav'")

        # Play back the response
        play_audio_file("generated_output.wav")
        
        os.remove(audio_data_file)
        os.remove("generated_output.wav")

if __name__ == "__main__":
    main()
