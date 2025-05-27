import time
import subprocess

# Build aralığı (saniye cinsinden)
BUILD_INTERVAL = 60 * 10  # 10 dakika (600 saniye)

def build_ursus():
    print("🔄 Ursus static site build başlıyor...")
    try:
        # Ursus CLI komutu ile build
        result = subprocess.run(["ursus"], capture_output=True, text=True)
        print("Ursus çıktı:", result.stdout)
        if result.stderr:
            print("Hata:", result.stderr)
        print("✅ Ursus static site build tamamlandı.")
    except Exception as e:
        print("❌ Ursus build sırasında hata:", e)

def main():
    while True:
        build_ursus()
        print(f"⏰ {BUILD_INTERVAL} saniye bekleniyor...")
        time.sleep(BUILD_INTERVAL)

if __name__ == "__main__":
    main()
