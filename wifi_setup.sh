#!/bin/bash

# Set your WiFi SSID and password
SSID="cyberlab24"
PASSWORD="IoTNetwork1234"

# Edit the wpa_supplicant.conf file to configure WiFi for Australia (AU)
sudo cat <<EOL > /etc/wpa_supplicant/wpa_supplicant.conf
country=AU
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid="$SSID"
    psk="$PASSWORD"
}
EOL

# Restart the networking service to apply changes
sudo systemctl restart networking