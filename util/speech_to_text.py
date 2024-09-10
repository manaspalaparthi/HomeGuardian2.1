import pyaudio
import json
from vosk import Model, KaldiRecognizer

# sudo apt-get install python3-pyaudio
# pip3 install vosk
#
# wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
# unzip vosk-model-small-en-us-0.15.zip

# Load Vosk model
model = Model("vosk-model-small-en-us-0.15")  # Path to the model


# Function to continuously record audio and convert speech to text
def record_and_convert_to_text():
    recognizer = KaldiRecognizer(model, 16000)  # Initialize recognizer with 16kHz sample rate
    mic = pyaudio.PyAudio()

    # Open stream for recording
    stream = mic.open(format=pyaudio.paInt16,  # 16-bit resolution
                      channels=1,  # Mono channel
                      rate=16000,  # Sampling rate of 16kHz (needed for Vosk)
                      input=True,  # Enable input (microphone)
                      frames_per_buffer=8192)  # Buffer size

    stream.start_stream()

    print("Listening...")

    while True:
        data = stream.read(4096, exception_on_overflow=False)  # Read data from mic
        if recognizer.AcceptWaveform(data):  # If recognizer returns a result
            result = json.loads(recognizer.Result())
            print(f"You said: {result['text']}")  # Extract the text from result


# Start recording and converting to text
record_and_convert_to_text()
