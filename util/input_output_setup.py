import pyaudio

# Initialize PyAudio
p = pyaudio.PyAudio()

# List available devices
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"Device {i}: {info['name']}")

# Close PyAudio
p.terminate()
