import os
import time
import linuxcnc
import subprocess

# 1. Securely fetch the API Key set in the operating system environment
BOB_API_KEY = os.environ.get("BOB_API_KEY")

if not BOB_API_KEY:
    print("❌ [FATAL ERROR]: IBM Bob API Key not found in the system!")
    print("Run this command in the terminal:")
    print('export BOB_API_KEY="your_secret_key"')
    exit(1)

def analyze_gcode_with_bob(filepath):
    """Reads the G-code header and sends it to IBM Bob CLI for safety auditing."""
    try:
        # Optimization: Only read the first 50 lines (header & setup) 
        # to avoid overloading the AI processing
        with open(filepath, 'r') as file:
            lines = [next(file) for _ in range(50) if file]
        gcode_snippet = "".join(lines)
        
        # Combine system instructions and CNC code into a single prompt text
        prompt_text = (
            "You are a CNC machine safety auditor. Analyze the following G-code snippet. "
            "Check if the feed rates (F) and axis movements (G0/G1) are safe. "
            "Provide a brief answer: SAFE with reasons, or DANGER with warnings.\n\n"
            f"Please check this G-code:\n{gcode_snippet}"
        )
        
        # CLI execution format: bob run "prompt"
        result = subprocess.run(
            ["bob", "run", prompt_text],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Retrieve text output from Bob Shell
        ai_message = result.stdout.strip()
        return f"🛡️ [IBM BOB AUDIT RESULT]:\n{ai_message}"
        
    except subprocess.CalledProcessError as e:
        return f"⚠️ [BOB CLI ERROR]: Process failed with code {e.returncode}\nDetails: {e.stderr.strip()}"
    except FileNotFoundError:
        return "❌ [SYSTEM ERROR]: The 'bob' application was not found on this system. Ensure IBM Bob Shell is installed."
    except Exception as e:
        return f"❌ [AUDIT ERROR]: {str(e)}"

def get_active_gcode_file():
    """Automatically detects the currently active G-code file in LinuxCNC."""
    s = linuxcnc.stat()
    print("🚀 [SYSTEM] Initializing CNC Node (ZeroMQ Subscriber)...")
    time.sleep(1)
    print("⏳ [AI AUDIT] Waiting for the operator to open a design file in the Milling interface...")
    
    while True:
        try:
            s.poll()
            if s.file and s.file.strip():
                print(f"\n✅ [SUCCESS] File detected: {s.file}")
                print("🔍 [AI AUDIT] Requesting safety clearance from IBM Bob 2.0...")
                
                # Using the new CLI function
                audit_result = analyze_gcode_with_bob(s.file)
                print(audit_result)
                
                # Optional safety logic: 
                # If you want the machine to STOP if the AI replies DANGER, you can add string checking here.
                
                return s.file
        except Exception as e:
            pass
        time.sleep(1)

if __name__ == "__main__":
    print("======================================================")
    print(" 🤖 LINUXCNC PRE-FLIGHT ASSISTANT (IBM BOB 2.0)       ")
    print("======================================================")
    
    file_path = get_active_gcode_file()
    
    if file_path and os.path.exists(file_path):
        print("======================================================")
        print(f"⚙️ [EXECUTION] Firing movement vectors to the machine...")
        print("======================================================")
    else:
        print("❌ [ERROR] Invalid or missing G-code file.")
