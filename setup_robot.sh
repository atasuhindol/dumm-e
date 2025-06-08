#!/bin/bash

echo "🚀 Raspberry Pi Robot Kurulumu Başlıyor (venv YOK, sistem içi kurulum)..."

# Python pip kısıtlamasını kaldır
echo "🔓 pip koruması (EXTERNALLY-MANAGED) kaldırılıyor..."
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
sudo rm -f /usr/lib/python${PYTHON_VERSION}/EXTERNALLY-MANAGED

# Sistem güncellemesi
echo "📦 Sistem güncelleniyor..."
sudo apt update && sudo apt upgrade -y

# Gerekli sistem kütüphaneleri
echo "📦 Temel bağımlılıklar kuruluyor..."
sudo apt install -y python3-pip python3-dev build-essential libatlas-base-dev \
                    libjpeg-dev libqtgui4 libqt4-test libqtcore4 \
                    libavformat-dev libswscale-dev libv4l-dev \
                    libopenblas-dev liblapack-dev libhdf5-dev \
                    libportaudio2 portaudio19-dev libasound2-dev \
                    libcamera-dev i2c-tools git

# GPIO ve Kamera aktivasyonu (raspi-config headless)
echo "🛠️ GPIO ve Kamera etkinleştiriliyor..."
sudo raspi-config nonint do_camera 0
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0

# Python kütüphaneleri kuruluyor
echo "🐍 Python pip kütüphaneleri kuruluyor (sistem geneli)..."
sudo pip3 install --upgrade pip
sudo pip3 install \
    numpy \
    opencv-python \
    tflite-runtime \
    gpiozero \
    RPi.GPIO \
    adafruit-blinka \
    adafruit-circuitpython-ssd1306 \
    adafruit-circuitpython-mpu6050 \
    adafruit-circuitpython-vl53l0x \
    SpeechRecognition \
    pyaudio \
    pyttsx3

# Test mesajı
echo "✅ Kurulum tamamlandı. Cihazı yeniden başlatmanız önerilir."
