#!/bin/bash

echo "🚀 Preparing Pre-Flight Assistant System..."

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# 1. Start the Muscle (Subscriber) silently in the background
python3 cnc_subscriber.py &
SUBSCRIBER_PID=$!

# 2. Start the AI Brain and display pop-up to the operator
python3 pre_flight_ai.py

# 3. Automatically kill the Muscle if the AI window finishes or is closed
kill $SUBSCRIBER_PID
exit 0
