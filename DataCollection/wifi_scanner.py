import cv2
import numpy as np
import os
import subprocess
from pyzbar.pyzbar import decode


def connect_to_wifi(ssid, password):
    # This function is for Unix-based systems like Linux or macOS.
    # For Windows, you need to use netsh commands.
    try:
        # Create a Wi-Fi configuration file
        config = f"""
        network={{
            ssid="{ssid}"
            psk="{password}"
        }}
        """
        config_path = "/etc/wpa_supplicant/wpa_supplicant.conf"

        with open(config_path, "w") as file:
            file.write(config)

        # Restart the Wi-Fi interface to apply changes
        subprocess.run(["sudo", "wpa_cli", "-i", "wlan0", "reconfigure"], check=True)
        print(f"Connected to {ssid}")
    except Exception as e:
        print(f"Failed to connect to {ssid}: {e}")


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

        cv2.imshow("QR Code Scanner", frame)
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


def main():
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


if __name__ == "__main__":
    main()
