import os
from pydub import AudioSegment, playback
import whisper  # From https://github.com/openai/whisper
import requests
import numpy as np
import io
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech
from datasets import load_dataset
import sounddevice as sd
from scipy.io.wavfile import write

# Configuration variables
WAKE_WORD = "raptor"
OLLAMA_URL = "http://localhost:8080"
LANGUAGE_CODE = "en"  # Language code for Whisper and TTS models (e.g., 'en' for English)

# TTS_MODEL_NAME: Name of the text-to-speech model to use
TTS_MODEL_NAME = "rafalosa/tts_difussor_male"  # Example: Use a male British voice

# Load Whisper model
model = whisper.load_model("base")

def transcribe_audio(audio_file):
    result = model.transcribe(audio_file, fp16=False)  # Set fp16 to True if running on GPU
    return result["text"]

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
    processor = SpeechT5Processor.from_pretrained(model_name)
    model = SpeechT5ForTextToSpeech.from_pretrained(model_name)

    inputs = processor(text=text, return_tensors="pt")
    speech = model.generate(**inputs).waveform[0].numpy()

    # Convert to AudioSegment
    audio_segment = AudioSegment(speech.tobytes(), frame_rate=16000, sample_width=2, channels=1)
    
    return audio_segment

def listen_for_wake_word(wake_word=WAKE_WORD):
    CHUNK_SIZE = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE)
    
    print(f"Listening for wake word '{wake_word}'...")
    
    frames = []
    
    while True:
        data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
        
        # Convert byte data to numpy array
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        # Perform detection (for simplicity, we're just checking if the wake word is spoken)
        text = transcribe_audio(io.BytesIO(audio_data.tobytes()))
        
        frames.append(data)

        if wake_word in text:
            print(f"Detected wake word: '{wake_word}'")
            
            stream.stop_stream()
            stream.close()
            p.terminate()

            # Save the recorded audio
            wf = wave.open('temp_audio.wav', 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            return 'temp_audio.wav'
    
    stream.stop_stream()
    stream.close()
    p.terminate()

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
        transcribed_text = transcribe_audio(audio_data_file)
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
