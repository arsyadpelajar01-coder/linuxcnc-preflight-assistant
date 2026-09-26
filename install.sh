#!/bin/bash

echo "📥 Downloading LinuxCNC Pre-Flight Assistant..."

# Move to the user's home directory
cd ~

# Remove previous installation if it exists to prevent conflicts
rm -rf linuxcnc-preflight-assistant linuxcnc-preflight-assistant-main

# Download archive (tar.gz) directly from GitHub without requiring Git
wget -qO- https://github.com/arsyadpelajar01-coder/linuxcnc-preflight-assistant/archive/refs/heads/main.tar.gz | tar xz

# Rename extracted directory to the target project name
mv linuxcnc-preflight-assistant-main linuxcnc-preflight-assistant
cd linuxcnc-preflight-assistant

echo "⚙️ Setting up permissions..."
# Make bash scripts executable
chmod +x start_assistant.sh
chmod +x run_all.sh

echo "🖥️ Creating Desktop shortcut..."
# Resolve the user's Desktop directory path
DESKTOP_DIR=$(xdg-user-dir DESKTOP 2>/dev/null || echo "$HOME/Desktop")
SHORTCUT="$DESKTOP_DIR/PreFlight_AI.desktop"

# Generate Linux desktop entry configuration
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

# Make the desktop shortcut executable
chmod +x "$SHORTCUT"

echo "======================================================"
echo " ✅ INSTALLATION COMPLETE! "
echo " You can now double-click 'Pre-Flight AI' on your Desktop."
echo "======================================================"
