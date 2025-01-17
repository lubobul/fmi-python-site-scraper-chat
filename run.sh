#!/bin/bash

# Function to handle termination
terminate() {
    echo "Terminating background processes..."
    kill 0
    exit 0
}

# Trap the SIGINT signal (Ctrl + C) to call the terminate function
trap terminate SIGINT

# Start the processes in the background
python3 app.py &
python3 fmi_website_proxy.py &
cd ./chat-ui && npm start &

# Wait for all background processes to complete
wait
