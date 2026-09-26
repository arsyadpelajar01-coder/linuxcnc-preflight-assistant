# 🚀 LinuxCNC Pre-Flight Assistant (IBM Bob 2.0)

A cognitive safety bridge between AI decision-making and industrial machine (CNC) execution. Built specifically for the IBM Bob 2.0 Hackathon to perform automated safety audits before the machine is allowed to move.

## ✨ Key Features

* **Auto G-Code Detection:** Reads the file opened by the operator in real-time directly from the LinuxCNC interface without requiring manual terminal input.
* **AI Safety Audit:** Verifies cutting parameters and machine safety boundaries (software limits) using IBM Bob 2.0 prior to execution.
* **Zero-Touch Operator Experience:** Supports desktop shortcut integration so CNC operators can work purely using the GUI (graphical user interface) naturally.

## 📋 Prerequisites

Before installing, ensure your Debian/LinuxCNC machine has the following configured:
1. **IBM Bob Shell:** Installed on the system (`bob` command available).
2. **API Key:** Set your environment variable by running:
   `export BOB_API_KEY="your_secret_key"`

## 📥 1-Click Installation

You do not need to manually clone this repository. Simply open your Linux terminal and run this single command to download the assistant and automatically generate a Desktop shortcut:

```bash
wget -qO- [https://raw.githubusercontent.com/arsyadpelajar01-coder/linuxcnc-preflight-assistant/main/install.sh](https://raw.githubusercontent.com/arsyadpelajar01-coder/linuxcnc-preflight-assistant/main/install.sh) | bash
