import zmq
import linuxcnc
import time

def main():
    print("Setting up CNC Node (ZeroMQ Subscriber)...")
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind("tcp://127.0.0.1:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    machine = linuxcnc.command()
    status = linuxcnc.stat()
    print("✅ Connected to LinuxCNC core. Waiting for AI instructions...")

    while True:
        try:
            msg = socket.recv_string()
            gcode_lines = msg.strip().split('\n')
            
            status.poll()
            if status.task_mode != linuxcnc.MODE_MDI:
                machine.mode(linuxcnc.MODE_MDI)
                machine.wait_complete()
                
            print("🚀 Starting maneuver execution:")
            # Executing line by line for stability in LinuxCNC
            for line in gcode_lines:
                command = line.strip()
                if command:
                    print(f"-> Moving: {command}")
                    machine.mdi(command)
                    machine.wait_complete()
                    time.sleep(0.1)
                    
            print("✅ Propeller cutting complete!")
            
        except KeyboardInterrupt:
            print("\nShutting down CNC Node...")
            break
        except Exception as e:
            print(f"⚠️ Execution error: {e}")

if __name__ == "__main__":
    main()
