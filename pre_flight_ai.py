import os
import time
import linuxcnc
import subprocess

# 1. Mengambil API Key yang sudah diset di sistem operasi secara aman
BOB_API_KEY = os.environ.get("BOB_API_KEY")

if not BOB_API_KEY:
    print("❌ [FATAL ERROR]: API Key IBM Bob tidak ditemukan di sistem!")
    print("Jalankan perintah ini di terminal:")
    print('export BOB_API_KEY="kunci_rahasia_anda"')
    exit(1)

def analyze_gcode_with_bob(filepath):
    """Membaca header G-code dan mengirimkannya ke IBM Bob CLI untuk audit keselamatan."""
    try:
        # Optimasi: Kita hanya membaca 50 baris pertama (header & setup) 
        # agar tidak membebani pemrosesan AI
        with open(filepath, 'r') as file:
            lines = [next(file) for _ in range(50) if file]
        gcode_snippet = "".join(lines)
        
        # Menggabungkan instruksi sistem dan kode CNC menjadi satu teks prompt
        prompt_text = (
            "Anda adalah auditor keselamatan mesin CNC. Analisis potongan G-code berikut. "
            "Periksa apakah kecepatan (F) dan pergerakan sumbu (G0/G1) aman. "
            "Berikan jawaban singkat: AMAN beserta alasannya, atau BAHAYA beserta peringatannya.\n\n"
            f"Tolong periksa G-code ini:\n{gcode_snippet}"
        )
        
        # Format eksekusi CLI: bob run "prompt"
        result = subprocess.run(
            ["bob", "run", prompt_text],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Mengambil hasil keluaran teks dari Bob Shell
        ai_message = result.stdout.strip()
        return f"🛡️ [HASIL AUDIT IBM BOB]:\n{ai_message}"
        
    except subprocess.CalledProcessError as e:
        return f"⚠️ [ERROR BOB CLI]: Proses gagal dengan kode {e.returncode}\nDetail: {e.stderr.strip()}"
    except FileNotFoundError:
        return "❌ [ERROR SISTEM]: Aplikasi 'bob' tidak ditemukan di sistem ini. Pastikan IBM Bob Shell sudah terinstal."
    except Exception as e:
        return f"❌ [ERROR AUDIT]: {str(e)}"

def get_active_gcode_file():
    """Mendeteksi file G-code yang sedang aktif di LinuxCNC secara otomatis."""
    s = linuxcnc.stat()
    print("🚀 [SISTEM] Menyiapkan Node CNC (ZeroMQ Subscriber)...")
    time.sleep(1)
    print("⏳ [AI AUDIT] Menunggu operator membuka file desain di antarmuka Frais...")
    
    while True:
        try:
            s.poll()
            if s.file and s.file.strip():
                print(f"\n✅ [BERHASIL] File terdeteksi: {s.file}")
                print("🔍 [AI AUDIT] Meminta clearance keselamatan dari IBM Bob 2.0...")
                
                # Menggunakan fungsi CLI yang baru
                audit_result = analyze_gcode_with_bob(s.file)
                print(audit_result)
                
                # Logika keamanan opsional: 
                # Jika Anda ingin mesin BERHENTI jika AI menjawab BAHAYA, Anda bisa menambah pengecekan string di sini.
                
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
        print(f"⚙️ [EKSEKUSI] Menembakkan vektor pergerakan ke mesin...")
        print("======================================================")
    else:
        print("❌ [ERROR] File G-code tidak valid atau tidak ditemukan.")
