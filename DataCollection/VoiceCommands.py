import threading
import requests
import pyaudio
import json
from vosk import Model, KaldiRecognizer
from camera import WebcamStream




class SpeechCommandHandler:
    def __init__(self):
        self.api_base_url = "http://localhost:8000"  # Base URL for your FastAPI server

    def execute_command(self, command):
        print(command)
        if "start recording" in command.lower():
            response = requests.get(f"{self.api_base_url}/start_recording")
            print(response.json())
        elif "stop recording" in command.lower():
            response = requests.get(f"{self.api_base_url}/stop_recording")
            print(response.json())
        elif "assign device id" in command.lower():
            device_id = self.extract_device_id(command)
            response = requests.get(f"{self.api_base_url}/assign_device_id?device_id={device_id}")
            print(response.json())
        else:
            print("Command not recognized")

    def extract_device_id(self, command):
        # Simple extraction assuming command format includes device_id explicitly
        import re
        match = re.search(r'\d+', command)
        return int(match.group()) if match else 0
def start_speech_command_handler():
    command_handler = SpeechCommandHandler()

    # Load Vosk model
    model = Model("models/vosk-model-small-en-us-0.15")  # Path to the model

    recognizer = KaldiRecognizer(model, 16000)  # Initialize recognizer with 16kHz sample rate
    mic = pyaudio.PyAudio()

    # Open stream for recording
    stream = mic.open(format=pyaudio.paInt16,  # 16-bit resolution
                      channels=1,  # Mono channel
                      rate=16000,  # Sampling rate of 16kHz (needed for Vosk)
                      input=True,  # Enable input (microphone)
                      frames_per_buffer=8192)  # Buffer size

    stream.start_stream()
    print("Listening for commands...")

    while True:
        data = stream.read(4096, exception_on_overflow=False)  # Read data from mic
        if recognizer.AcceptWaveform(data):  # If recognizer returns a result
            result = json.loads(recognizer.Result())
            command = result['text']
            print(f"Command received: {command}")
            command_handler.execute_command(command)


if __name__ == "__main__":
    # Start the command handler in a separate thread
    command_handler_thread = threading.Thread(target=start_speech_command_handler)
    command_handler_thread.start()
