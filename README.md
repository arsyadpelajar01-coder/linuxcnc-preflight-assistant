# 🚀 LinuxCNC Pre-Flight Assistant (IBM Bob 2.0)

A cognitive safety bridge between AI decision-making and industrial machine (CNC) execution. Built specifically for the IBM Bob 2.0 Hackathon to perform automated safety audits before the machine is allowed to move.

## ✨ Key Features
- **Auto G-Code Detection:** Reads the file opened by the operator in *real-time* directly from the LinuxCNC interface without requiring manual terminal input.
- **AI Safety Audit:** Verifies cutting parameters and machine safety boundaries (*software limits*) using IBM Bob 2.0 prior to execution.
- **Zero-Touch Operator Experience:** Supports *desktop shortcut* integration so CNC operators can work purely using the GUI (graphical user interface) naturally.

## ⚙️ Usage Guide
1. Ensure you have a configured LinuxCNC (Debian) environment.
2. *Clone* this repository:
   `git clone https://github.com/arsyadpelajar01-coder/linuxcnc-preflight-assistant.git`
3. Grant execution permissions to the scripts:
   `chmod +x run_all.sh start_assistant.sh`
4. Run the system with just a single command (or link it to a *desktop shortcut*):
   `./run_all.sh`
