import zmq
import linuxcnc
import time

def main():
    print("Menyiapkan Node CNC (ZeroMQ Subscriber)...")
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind("tcp://127.0.0.1:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    mesin = linuxcnc.command()
    status = linuxcnc.stat()
    print("✅ Terhubung dengan inti LinuxCNC. Menunggu instruksi AI...")

    while True:
        try:
            msg = socket.recv_string()
            gcode_lines = msg.strip().split('\n')
            
            status.poll()
            if status.task_mode != linuxcnc.MODE_MDI:
                mesin.mode(linuxcnc.MODE_MDI)
                mesin.wait_complete()
                
            print("🚀 Mulai mengeksekusi manuver:")
            # Mengeksekusi baris demi baris agar stabil di LinuxCNC
            for baris in gcode_lines:
                perintah = baris.strip()
                if perintah:
                    print(f"-> Bergerak: {perintah}")
                    mesin.mdi(perintah)
                    mesin.wait_complete()
                    time.sleep(0.1)
                    
            print("✅ Pemotongan propeler selesai!")
            
        except KeyboardInterrupt:
            print("\nMematikan Node CNC...")
            break
        except Exception as e:
            print(f"⚠️ Error eksekusi: {e}")

if __name__ == "__main__":
    main()
