#!/bin/bash

# Define the destination directory where the .service files are stored
DEST_DIR="/etc/systemd/system"

# Get the directory where this script is located (assumed to be the same as the .service files)
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Loop through all .service files in the source directory
for service_file in $SOURCE_DIR/*.service; do
    service_name=$(basename $service_file)

    # Stop the service
    echo "Stopping $service_name..."
    sudo systemctl stop $service_name

    # Disable the service from starting at boot
    echo "Disabling $service_name..."
    sudo systemctl disable $service_name
done

# Reload systemd to apply the changes
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "All services have been stopped and disabled."
