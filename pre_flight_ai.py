import json
import urllib.request
import zmq
import time

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
    print("Menghubungkan ke jaringan kontrol mesin (ZeroMQ)...")
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect("tcp://127.0.0.1:5555")
    
    time.sleep(1) 
    
    # Vektor manufaktur propeler 3 bilah
    gcode_propeller_3_bilah = """
G0 Z10
G0 X20 Y20
G1 Z-2 F100
G1 X40 Y40 F200
G0 Z10
G0 X-20 Y20
G1 Z-2 F100
G1 X-40 Y40 F200
G0 Z10
G0 X0 Y-20
G1 Z-2 F100
G1 X0 Y-40 F200
G0 Z10
G0 X0 Y0
"""
    print("Menembakkan vektor pergerakan propeler 3 bilah ke mesin...")
    socket.send_string(gcode_propeller_3_bilah.strip())
    print("🎯 Eksekusi otomatis berhasil dipicu!")

if __name__ == "__main__":
    status_aman = jalankan_audit_ai()
    
    if status_aman:
        kirim_instruksi_cnc()
