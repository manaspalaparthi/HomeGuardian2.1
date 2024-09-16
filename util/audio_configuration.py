import os
import time

def configure_usb_audio(card_number):
    # Path to the ALSA configuration file
    asound_conf_path = '/etc/asound.conf'

    # The content to be written to the configuration file
    asound_conf_content = f"""
pcm.!default {{
    type hw
    card {card_number}
}}

ctl.!default {{
    type hw
    card {card_number}
}}
"""

    try:
        # Write the configuration content to the file
        with open(asound_conf_path, 'w') as conf_file:
            conf_file.write(asound_conf_content)

        print(f"Audio configuration updated to use card {card_number}")

        # Restart ALSA to apply the new settings
        os.system('sudo systemctl restart alsa')

        print("ALSA restarted. The new audio configuration should now be active.")

    except PermissionError:
        print("Permission denied: Run this script with sudo.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Set the audio card number (replace this if the card number changes)
    configure_usb_audio(4)
    time.sleep(5)

