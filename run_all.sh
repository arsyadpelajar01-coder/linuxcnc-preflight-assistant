#!/bin/bash
cd /home/linuxcnc/linuxcnc-preflight-assistant
./start_assistant.sh &
linuxcnc /home/linuxcnc/linuxcnc/configs/Frais_AI/Frais_AI.ini
