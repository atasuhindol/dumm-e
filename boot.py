import startup.system_check as system_check
from controllers.display_controller import DisplayController

def boot_sequence():
    print("🚀 Robot başlatılıyor...")
    
    # Donanım kontrolleri
    print("🔧 Donanım testleri yapılıyor...")
    if not system_check.run_all_tests():
        print("❌ Donanım testi başarısız! Lütfen kontrol et.")
        # İstersen burada hata durumunda sistemi durdurabilirsin.
        return False
    
    # Ekran açılıyor
    display = DisplayController()
    display.init_display()
    display.show_message("Robot Başladı!")
    
    print("✅ Başlangıç başarılı.")
    return True

if __name__ == "__main__":
    boot_sequence()
