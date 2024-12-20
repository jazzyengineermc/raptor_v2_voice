from tracemalloc import start
import subprocess as cmdLine
import os

speech = 'This is what I have to say... ha ha, ho ho, he he, ha ha'
voicef = 'mb-us1 ' # For female voice
voicem = 'mb-us2 ' # For Male voice
vmbrit = 'mb-en1 ' # Male Brittish Voice
voice = vmbrit

class Espeak:
    def __init__(self):
        pass

    def talk(self, voice, speech):
        command = 'espeak -v '+ voice + chr(34) + speech + chr(34) + ' -s 145'
        result = cmdLine.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)