#!/bin/bash

# 🔥 Otomatis matikan proses subscriber yang nyangkut di port 5555
pkill -f cnc_subscriber.py 2>/dev/null || true
sleep 1

# 1. Load existing key if available
if [ -f "$HOME/.bob_api_key" ]; then
    source "$HOME/.bob_api_key"
fi

# 2. Require non-empty input
while [ -z "$BOB_API_KEY" ]; do
    echo "⚠️ IBM Bob API Key is missing or empty!"
    read -p "Please paste your API Key here and press Enter: " input_key
    
    if [ -n "$input_key" ]; then
        echo "export BOB_API_KEY=\"$input_key\"" > "$HOME/.bob_api_key"
        export BOB_API_KEY="$input_key"
        echo "✅ API Key saved successfully!"
        echo "------------------------------------------------------"
    else
        echo "❌ Error: API Key cannot be empty. Please try again."
        echo ""
    fi
done

echo "🚀 Preparing Pre-Flight Assistant System..."

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

python3 cnc_subscriber.py &
SUBSCRIBER_PID=$!

python3 pre_flight_ai.py

kill $SUBSCRIBER_PID
exit 0
