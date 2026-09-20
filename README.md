# LinuxCNC Pre-Flight Assistant 🚀

A cognitive safety bridge between AI decision-making and industrial machine execution. Built for the IBM Bob 2.0 Hackathon.

## Overview
This project introduces an automated "Pre-Flight" audit system for industrial 3-Axis milling machines. Before executing complex maneuvers, the system securely transmits machine configurations (`.hal` & `.ini`) and G-Code logic to **IBM Bob 2.0**. The AI analyzes the payload against safety manuals to detect pin logic conflicts or velocity violations.

The demonstration payload features a precision G-Code maneuver for manufacturing a balanced 3-blade propeller, designed to symbolize the three members of our group. 

If clearance is granted, the system utilizes a high-speed ZeroMQ (ZMQ) Publisher/Subscriber architecture to instantly trigger the hardware execution natively within the LinuxCNC environment.

## Architecture
1. **The Brain (`pre_flight_ai.py`):** Acts as the cognitive gateway. It handles API communication with IBM Bob 2.0 and acts as a ZMQ Publisher to dispatch validated G-Code.
2. **The Muscle (`cnc_subscriber.py`):** Runs natively inside the Debian/LinuxCNC virtual environment. It operates as a ZMQ Subscriber, converting network payloads directly into MDI commands via the `linuxcnc` HAL Python API.

## About the Developer
Developed by Arsyad Mulya Rahman, integrating principles of Mechanical Engineering from Universitas Andalas with modern AI automation to enhance industrial safety.

## Quick Start
1. Start the machine environment and ensure it is powered ON (E-Stop disabled).
2. Run the hardware execution node in a terminal:
   ```bash
   python3 cnc_subscriber.py
