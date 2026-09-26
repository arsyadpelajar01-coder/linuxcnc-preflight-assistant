#!/bin/bash

echo "📥 Downloading LinuxCNC Pre-Flight Assistant..."

# Pindah ke direktori Home
cd ~

# Hapus instalasi lama jika ada untuk menghindari konflik
rm -rf linuxcnc-preflight-assistant linuxcnc-preflight-assistant-main

# Unduh versi arsip (tar.gz) langsung dari GitHub (Tanpa menggunakan Git)
wget -qO- https://github.com/arsyadpelajar01-coder/linuxcnc-preflight-assistant/archive/refs/heads/main.tar.gz | tar xz

# Ubah nama folder hasil ekstrak agar sesuai
mv linuxcnc-preflight-assistant-main linuxcnc-preflight-assistant
cd linuxcnc-preflight-assistant

echo "⚙️ Setting up permissions..."
# Jadikan skrip bash bisa dieksekusi
chmod +x start_assistant.sh
chmod +x run_all.sh

echo "🖥️ Creating Desktop shortcut..."
# Path ke Desktop pengguna di Linux
DESKTOP_DIR=$(xdg-user-dir DESKTOP 2>/dev/null || echo "$HOME/Desktop")
SHORTCUT="$DESKTOP_DIR/PreFlight_AI.desktop"

# Membuat file konfigurasi aplikasi Linux
cat > "$SHORTCUT" << EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=Pre-Flight AI
Comment=IBM Bob 2.0 Safety Auditor for LinuxCNC
Exec=bash -c "cd $HOME/linuxcnc-preflight-assistant && ./start_assistant.sh; exec bash"
Icon=utilities-terminal
Terminal=true
Categories=Utility;Engineering;
EOL

# Jadikan ikon di desktop bisa diklik
chmod +x "$SHORTCUT"

echo "======================================================"
echo " ✅ INSTALLATION COMPLETE! "
echo " You can now double-click 'Pre-Flight AI' on your Desktop."
echo "======================================================"
