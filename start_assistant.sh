#!/bin/bash

# 1. Sistem Cerdas Pembaca API Key
# Cek apakah kunci sudah pernah disimpan di file tersembunyi sebelumnya
if [ -f "$HOME/.bob_api_key" ]; then
    source "$HOME/.bob_api_key"
fi

# Jika masih kosong, minta input langsung dari juri/operator di dalam terminal aplikasi
if [ -z "$BOB_API_KEY" ]; then
    echo "⚠️ IBM Bob API Key is missing!"
    read -p "Please paste your API Key here and press Enter: " input_key
    # Simpan secara permanen agar tidak ditanya lagi saat dibuka besok
    echo "export BOB_API_KEY=\"$input_key\"" > "$HOME/.bob_api_key"
    export BOB_API_KEY="$input_key"
    echo "✅ API Key saved successfully!"
    echo "------------------------------------------------------"
fi

echo "🚀 Preparing Pre-Flight Assistant System..."

# Dapatkan direktori tempat skrip ini berada
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# 2. Nyalakan Otot (Subscriber) di latar belakang secara diam-diam
python3 cnc_subscriber.py &
SUBSCRIBER_PID=$!

# 3. Nyalakan Otak AI
python3 pre_flight_ai.py

# 4. Matikan Otot jika jendela ditutup
kill $SUBSCRIBER_PID
exit 0
