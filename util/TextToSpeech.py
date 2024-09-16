

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

def text_to_speech(txt, save=False, filename="output.mp3"):
    try:
        # Create TTS object
        tts = gTTS(txt)

        # Save or create temporary file
        if save:
            tts.save(filename)
        else:
            filename = "temp.mp3"
            tts.save(filename)

        # Initialize pygame mixer
        pygame.mixer.init()

        # Load and play the mp3 file
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        # Wait for the playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)

        # Cleanup the temporary mp3 file if save=False
        if not save:
            if os.path.exists(filename):
                os.remove(filename)

    except Exception as e:
        print(f"An error occurred: {e}")


# import pyttsx3

#
# def text_to_speech(text):
#     # Initialize the text-to-speech engine
#     engine = pyttsx3.init()
#
#     # Set properties (optional)
#     engine.setProperty('rate', 150)  # Speed of speech
#     engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
#
#     # Perform text-to-speech
#     engine.say(text)
#     engine.runAndWait()

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

    text_to_speech("video failed to upload, please restart the device and try again", save = True, filename = "../wav/failed.mp3")
