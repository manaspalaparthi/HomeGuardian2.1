#!/bin/bash

# Define the destination directory for the .service files
DEST_DIR="/etc/systemd/system"

# Get the directory where this script is located
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copy all .service files from the script's directory to the systemd folder
echo "Copying .service files from $SOURCE_DIR to $DEST_DIR..."
sudo cp $SOURCE_DIR/*.service $DEST_DIR/

# Reload systemd to recognize the new/updated services
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Optionally, enable and start each service
for service_file in $SOURCE_DIR/*.service; do
    service_name=$(basename $service_file)

    # Enable the service to start at boot
    echo "Enabling $service_name..."
    sudo systemctl enable $service_name

    # Start the service immediately
    echo "Starting $service_name..."
    sudo systemctl start $service_name
done

echo "All services have been copied, enabled, and started."

# run this chmod +x deploy_services.sh to make it executable