

import pygame
import os
from gtts import gTTS  # Google Text-to-Speech

# # Convert text to speech and save as mp3
# text = "IP address is 192.168.0.1:8000"
# tts = gTTS(text)

# filename = "wav/IP.mp3"
# tts.save(filename)

# # Initialize pygame mixer
# pygame.mixer.init()

# # Load and play the mp3 file
# pygame.mixer.music.load(filename)
# pygame.mixer.music.play()

# # Wait for the playback to finish
# while pygame.mixer.music.get_busy():
#     pygame.time.Clock().tick(10)

# # Cleanup the mp3 file
# #os.remove("wav/output.mp3")

# def text_to_speech(txt):
#     tts = gTTS(txt)
#     tts.save("temp.mp3")
#     # Initialize pygame mixer
#     pygame.mixer.init()
#
#     # Load and play the mp3 file
#     pygame.mixer.music.load("temp.mp3")
#     pygame.mixer.music.play()
#
#     # Wait for the playback to finish
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(1)
#
#     # Cleanup the mp3 file
#     os.remove("temp.mp3")


import pyttsx3


def text_to_speech(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

    # Perform text-to-speech
    engine.say(text)
    engine.runAndWait()



# Function to play audio using pygame.mixer
def play_audio(file_name):
    # Initialize pygame mixer
    pygame.mixer.init()

    # Load and play the audio file
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()
    # Wait until playback is finished
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

if __name__ == "__main__":

    text_to_speech("Home guardian is turned on, please scan a QR code to connect to wifi")
