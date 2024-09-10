import pyaudio
import wave
import pygame
import os

# Function to record audio from microphone
def record_audio(file_name, record_seconds=5, sample_rate=44100, channels=1, chunk=1024):
    p = pyaudio.PyAudio()

    # Open stream for recording
    stream = p.open(format=pyaudio.paInt16,  # 16-bit resolution
                    channels=channels,       # 1 channel (mono), change to 2 for stereo
                    rate=sample_rate,        # Sampling rate
                    input=True,              # Enable input (microphone)
                    frames_per_buffer=chunk) # Buffer size

    print(f"Recording for {record_seconds} seconds...")

    frames = []

    # Record for the specified time
    for _ in range(0, int(sample_rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print("Recording finished.")

    # Stop the stream and close PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a .wav file
    wf = wave.open(file_name, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function to play audio using pygame.mixer
def play_audio(file_name):
    # Initialize pygame mixer
    pygame.mixer.init()

    # Load and play the audio file
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()

    print("Playing audio...")

    # Wait until playback is finished
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    print("Playback finished.")

# File name to save the recorded audio
audio_file = "recorded_audio.wav"

# Record audio from mic
record_audio(audio_file, record_seconds=5)

# Play the recorded audio through the speaker
play_audio(audio_file)

# Optionally, delete the audio file after playing
os.remove(audio_file)
