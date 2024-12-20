#!/usr/bin/python3
from Espeak import *
import pyttsx3

# Mouth --- default old voice
engine = pyttsx3.init()
engine.setProperty("rate", 350)
        
vmbrit = 'mb-en1 ' # Male Brittish Voice

voice = vmbrit
es = Espeak()

es.talk(voice, speech='Greetings and salutations')