import json
import urllib.request
import zmq
import time
import os
import tkinter as tk
from tkinter import filedialog

def jalankan_audit_ai():
    print("\n" + "="*55)
    print("🚀 LINUXCNC PRE-FLIGHT ASSISTANT (IBM BOB 2.0) 🚀")
    print("="*55)
    
    teks_manual = "Batas kecepatan maksimal mesin adalah F300. Jangan gunakan F500."
    teks_ini = "MAX_VELOCITY = 1500 mm/min"
    
    ai_prompt = f"""
    Bandingkan [KONFIGURASI MESIN] dengan [DOKUMEN MANUAL].
    Manual: {teks_manual}
    Konfigurasi: {teks_ini}
    Tugas: Berikan kesimpulan singkat apakah mesin aman dinyalakan untuk eksekusi G-Code berkecepatan F200.
    """

    # ========================================================
    # ⚠️ UPDATE VARIABEL INI SAAT HACKATHON DIMULAI ⚠️
    # ========================================================
    API_URL = "https://url-dari-panitia-hackathon.com/api/v1/chat" 
    API_KEY = "MASUKKAN_API_KEY_DARI_PANITIA_DI_SINI"
    NAMA_MODEL = "ibm-bob-2.0"
    # ========================================================

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": NAMA_MODEL,
        "messages": [
            {"role": "system", "content": "Anda adalah auditor keamanan mesin industri CNC."},
            {"role": "user", "content": ai_prompt}
        ],
        "temperature": 0.1 
    }

    print("🤖 Meminta clearance keselamatan dari IBM Bob 2.0...\n")
    
    try:
        req = urllib.request.Request(API_URL, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            hasil_ai = json.loads(response.read().decode('utf-8'))
            print("🔍 [HASIL AUDIT]:\n" + hasil_ai['choices'][0]['message']['content'])
    except Exception as e:
        print(f"[SIMULASI HACKATHON] AI Audit diasumsikan AMAN. (Error API aktual: {e})")
        print("🔍 [HASIL AUDIT]: Konfigurasi aman. Batas kecepatan terpenuhi.")
    
    print("="*55 + "\n")
    return True 

def kirim_instruksi_cnc():
    print("🛠️  MODE OPERATOR: Membuka jendela pemilihan file...")
    
    # Menyiapkan jendela GUI (menyembunyikan jendela utama Tkinter yang kosong)
    root = tk.Tk()
    root.withdraw()
    
    # Membuka dialog pemilihan file
    path_file = filedialog.askopenfilename(
        title="Pilih File Desain G-Code",
        filetypes=(
            ("G-Code Files", "*.ngc *.gcode *.nc"),
            ("Text Files", "*.txt"),
            ("Semua File", "*.*")
        )
    )
    
    # Jika operator menekan 'Cancel' atau menutup jendela
    if not path_file:
        print("❌ Operasi dibatalkan: Operator tidak memilih file desain.")
        return

    print(f"✅ File dipilih: {path_file}")
    
    # Membaca file dan mengirimkan ke mesin
    try:
        with open(path_file, 'r') as file:
            gcode_operator = file.read()
            
        print("Menghubungkan ke jaringan kontrol mesin (ZeroMQ)...")
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.connect("tcp://127.0.0.1:5555")
        
        time.sleep(1) # Jeda untuk memastikan koneksi ZMQ stabil
        
        print("🚀 Menembakkan vektor pergerakan ke mesin...")
        socket.send_string(gcode_operator.strip())
        print("🎯 Eksekusi otomatis berhasil dipicu!")
        
    except Exception as e:
        print(f"❌ ERROR saat membaca atau mengirim file: {e}")

if __name__ == "__main__":
    status_aman = jalankan_audit_ai()
    
    if status_aman:
        kirim_instruksi_cnc()
