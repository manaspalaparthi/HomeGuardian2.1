import pyttsx3
import pygame
import time

def play_text(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def play_audio(file_path):
    # Initialize pygame mixer
    pygame.mixer.init()

    # Load and play the audio file
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(1)

if __name__ == "__main__":
    # Choose one of the options below:

    # Option 1: Play text as speech
    play_text("Hello, this is a test message played through the USB speaker!")

    # Option 2: Play an audio file
    # play_audio("/path/to/your/audiofile.mp3")
