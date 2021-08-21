"""
1. Relay connection to Device Live Wire
Normally Open - COM

2. Arduino Pins to Relay Channel
Channel IN1 -> 7 (Lamp)
Channel IN2 -> 8 (Lamp)
GND -> GND
VCC -> 5V

3. Libraries to install:
a) For Arduino Serial communication
!pip install pyfirmata

b) For capturing your voice
!pip install SpeechRecognition

c) For Bahasa Malaysia ML Model (Malaya-Speech)
!pip install networkx==2.5.1
!pip install malaya-speech

d) For saving Text-to-Speech generated Sound
!pip install SoundFile

"""
import malaya_speech
import numpy as np
from malaya_speech import Pipeline
import speech_recognition as spr
import soundfile as sf
import os
from time import sleep
import pyfirmata


def lamp_on():
    lamp.write(0)
def lamp_off():
    lamp.write(1)

def fan_on():
    fan.write(0)
def fan_off():
    fan.write(1)


def user_speak():
    print("Berikan arahan anda:")
    # setup mic 
    r = spr.Recognizer()
    mic = spr.Microphone()
    with mic as source:
        audio = r.listen(source)

        with open('speech.wav', 'wb') as f:
            f.write(audio.get_wav_data())

        try:
            userinput, sr = malaya_speech.load('speech.wav')
            text = model.greedy_decoder([userinput])
            return text[0]

        except spr.UnknownValueError:
            print("Maaf, sistem tidak dapat mengenal pasti percakapan anda...")

def system_speak(word):
    r_female = female.predict(word)
    y_ = vocoder_female(r_female['postnet-output'])
    sf.write('output.wav', y_, 20000)
    os.startfile('output.wav')
    sleep(4)

def check_instruction(userinput):
    print(userinput)
    if 'buka kipas' in userinput:
        system_speak("Baiklah, kipas akan dibuka. Sila tunggu.")
        fan_on()
        return True

    elif 'tutup kipas' in userinput:
        system_speak("Baiklah, kipas akan berhenti.")
        fan_off()
        return True

    if 'buka lampu' in userinput:
        system_speak("Baiklah, lampu akan dibuka. Sila tunggu.")
        lamp_on()
        return True

    elif 'tutup lampu' in userinput:
        system_speak("Baiklah, lampu akan ditutup.")
        lamp_off()
        return True

    elif 'tak ada'  in userinput:
        system_speak("Terima kasih kerana menggunakan saya.")
        return False

    else:
        system_speak("Maaf, arahan tidak jelas.")
        return True

# Check your Arduino COM Port    
board = pyfirmata.Arduino('COM8')
lamp = board.digital[7]
fan = board.digital[8]

# for safety, start with all device off
lamp_off()
fan_off()

# ML Model for Speech to Text from malaya_speech
model = malaya_speech.stt.deep_transducer(model = 'conformer')

# ML Model for Text to Speech from malaya_speech
female = malaya_speech.tts.fastspeech2(model = 'female')
vocoder_female = malaya_speech.vocoder.melgan(model = 'female')

print("======== SISTEM BIBIK ================")

system_speak("Hai, saya bibik. Boleh saya bantu awak?")
speech_input1 = user_speak()
isContinue = check_instruction(speech_input1)

while isContinue:
    sleep(5)
    system_speak("Ada lagi nak minta tolong?")
    speech_input2 = user_speak()
    isContinue = check_instruction(speech_input2)
