import cv2
import numpy as np
import os
import subprocess
from pyzbar.pyzbar import decode
import tempfile
from util.TextToSpeech import text_to_speech , play_audio
import socket
import time

def connect_to_wifi(ssid, password):
    # This function is for Unix-based systems like Linux or macOS.
    # For Windows, you need to use netsh commands.
    try:
        # Create a Wi-Fi configuration file
        config = f"""
        country=AU
        ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
        update_config=1
        network={{
            ssid="{ssid}"
            psk="{password}"
        }}
        """
        # start network manager
        os.system("sudo systemctl start NetworkManager")
        # Retry logic for nmcli command
        max_retries = 3
        retry_interval = 5  # Time to wait between retries in seconds

        for attempt in range(max_retries):
            cmd = f"sudo nmcli dev wifi connect '{ssid}' password '{password}'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print("Wi-Fi connected successfully.")
                break
            else:
                print(f"nmcli command failed: {result.stderr}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_interval} seconds...")
                    time.sleep(retry_interval)
        else:
            print("All attempts to connect to Wi-Fi failed. Proceeding with fallback method.")

            # Handle the failure case
            with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_config:
                temp_config.write(config)
                temp_config_path = temp_config.name

            # Move the temp file to the correct location with sudo and change permissions
            move_command = ["sudo", "mv", temp_config_path, "/etc/wpa_supplicant/wpa_supplicant.conf"]
            subprocess.run(move_command, check=True)

            # Restart networking service
            restart = ["sudo", "systemctl", "restart", "networking"]
            subprocess.run(restart, check=True)

        # Check if the device is connected to the Wi-Fi network by pinging Google's DNS server try 3 times
        for attempt in range(3):
            time.sleep(5)
            if check_internt_connection():
                print(f"Connected to {ssid}")
                break

        # Get the IP address
        ip_address = socket.gethostbyname(socket.gethostname())
        print(f"Ip address {ip_address}")
        text_to_speech(f"Connected to {ssid}. IP address is {ip_address}")

    except Exception as e:
        text_to_speech(f"Failed to connect to {ssid}")


def scan_qr_code():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        decoded_objects = decode(frame)
        for obj in decoded_objects:
            qr_data = obj.data.decode("utf-8")
            print(f"Decoded QR Code: {qr_data}")

            if qr_data.startswith("WIFI:"):
                wifi_info = parse_wifi_info(qr_data)
                cap.release()
                cv2.destroyAllWindows()
                return wifi_info

        #cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None


def parse_wifi_info(qr_data):
    # Example QR data format: WIFI:S:<SSID>;T:<WPA|WEP|>;P:<PASSWORD>;;
    wifi_info = {}
    data = qr_data[5:]  # Remove 'WIFI:'
    elements = data.split(';')
    for element in elements:
        if element.startswith('S:'):
            wifi_info['ssid'] = element[2:]
        elif element.startswith('T:'):
            wifi_info['type'] = element[2:]
        elif element.startswith('P:'):
            wifi_info['password'] = element[2:]
    return wifi_info


def WIFIconnect():
    time.sleep(10)
    if check_internt_connection():
        play_audio("wav/online.mp3")
        # text_to_speech("Home guardian is turned on and connected to wifi")
    else:
        play_audio("wav/scanQR.mp3")
        wifi_info = scan_qr_code()
        if wifi_info:
            ssid = wifi_info.get('ssid')
            password = wifi_info.get('password')
            if ssid and password:
                connect_to_wifi(ssid, password)
            else:
                print("Invalid Wi-Fi information found in QR code")
        else:
            print("No valid QR code found")

def check_internt_connection():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False
if __name__ == "__main__":
    WIFIconnect()
