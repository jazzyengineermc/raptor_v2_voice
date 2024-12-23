import pyaudio
from faster_whisper import WhisperModel

# Load a locally hosted model (make sure to download the model first)
model = WhisperModel("/home/jreide/faster-whisper/models/tiny")  # You can change "tiny" to another size like "base", "small", etc.
WAKE_WORD = "raptor"

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

def recognize_speech():
    text_answer = None

    while text_answer is None:
        data = stream.read(4000)
        if len(data) == 0:
            break
        
        # Convert the audio data to bytes array and pass it to fast-whisper for transcription.
        result = model.transcribe(bytearray(data))
        
        text = result['text'].lower()
        print(text)

        if WAKE_WORD in text:  # Assuming you have a variable `WAKE_WORD` defined somewhere
            text_answer = text.replace(WAKE_WORD, '')
            return text_answer

    stream.stop_stream()
    stream.close()
    p.terminate()

    return None


if __name__ == "__main__":
    recognize_speech()

    