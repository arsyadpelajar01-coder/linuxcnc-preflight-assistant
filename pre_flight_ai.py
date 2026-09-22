import os
import time
import linuxcnc

def get_active_gcode_file():
    """Mendeteksi file G-code yang sedang aktif/dibuka di LinuxCNC secara otomatis."""
    s = linuxcnc.stat()
    print("⏳ Menunggu operator membuka file G-code di LinuxCNC...")
    
    while True:
        try:
            s.poll()
            # s.file berisi path absolut dari file ngc yang sedang dimuat di LinuxCNC
            if s.file and s.file.strip():
                print(f"✔ File terdeteksi dari LinuxCNC: {s.file}")
                return s.file
        except Exception as e:
            pass
        time.sleep(1)

if __name__ == "__main__":
    print("========================================")
    print(" LINUXCNC PRE-FLIGHT ASSISTANT (AI)     ")
    print("========================================")
    
    # Ambil file secara otomatis langsung dari aplikasi LinuxCNC
    file_path = get_active_gcode_file()
    
    if file_path and os.path.exists(file_path):
        print(f"⚙ Menembakkan vektor pergerakan ke mesin untuk: {file_path}")
        # Lanjutkan proses audit / komunikasi ZeroMQ di sini...
    else:
        print("❌ Error: File G-code tidak ditemukan.")
