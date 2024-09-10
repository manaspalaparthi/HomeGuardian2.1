import pyaudio

# Initialize PyAudio
p = pyaudio.PyAudio()

# List available devices
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"Device {i}: {info['name']}")

# Close PyAudio
p.terminate()


import pygame
import os
from gtts import gTTS  # Google Text-to-Speech

# Convert text to speech and save as mp3
text = "Hello, your USB speaker is working!"
tts = gTTS(text)
tts.save("output.mp3")

# Initialize pygame mixer
pygame.mixer.init()

# Load and play the mp3 file
pygame.mixer.music.load("output.mp3")
pygame.mixer.music.play()

# Wait for the playback to finish
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

# Cleanup the mp3 file
#os.remove("output.mp3")
