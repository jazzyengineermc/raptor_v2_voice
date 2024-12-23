import requests
import subprocess as cmdLine

urlPiper = "http://localhost:5000"
outputFilename = "output.wav"


def tts_piper(textToSpeak):
    payload = {'text': textToSpeak}

    r = requests.get(urlPiper,params=payload)

    with open(outputFilename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
            
    command = 'play '+ outputFilename 
    result = cmdLine.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    
    
if __name__ == "__main__":
    textToSpeak = "This is a text to be spoken using the locally running Piper TTS server process."
    tts_piper(textToSpeak=textToSpeak)