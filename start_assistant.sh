#!/bin/bash

echo "🚀 Menyiapkan Sistem Pre-Flight Assistant..."

# Mendapatkan direktori tempat skrip ini berada
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# 1. Nyalakan Otot (Subscriber) di latar belakang secara diam-diam
python3 cnc_subscriber.py &
SUBSCRIBER_PID=$!

# 2. Nyalakan Otak AI dan tampilkan pop-up ke operator
python3 pre_flight_ai.py

# 3. Matikan Otot secara otomatis jika jendela AI selesai atau ditutup
kill $SUBSCRIBER_PID
exit 0
