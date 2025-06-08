"""
sensor_controller.py

Handles MPU6050 (gyroscope + accelerometer) and GY-530 (VL53L0X ToF distance) sensors.
Provides functions for orientation, tilt detection, and obstacle detection.
"""

import smbus2
import time

# MPU6050 registers and constants
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# VL53L0X I2C address (GY-530 default)
VL53L0X_ADDR = 0x29

# For VL53L0X, we'll use the adafruit_vl53l0x library for simplicity
try:
    import board
    import busio
    import adafruit_vl53l0x
except ImportError:
    print("[SensorController] adafruit_vl53l0x library not found. Distance sensor disabled.")

class MPU6050:
    def __init__(self, bus=1):
        self.bus = smbus2.SMBus(bus)
        self.addr = MPU6050_ADDR
        # Wake up MPU6050
        self.bus.write_byte_data(self.addr, PWR_MGMT_1, 0)
        time.sleep(0.1)
    
    def read_raw_data(self, reg):
        high = self.bus.read_byte_data(self.addr, reg)
        low = self.bus.read_byte_data(self.addr, reg+1)
        value = ((high << 8) | low)
        if value > 32768:
            value = value - 65536
        return value
    
    def get_acceleration(self):
        ax = self.read_raw_data(ACCEL_XOUT_H) / 16384.0
        ay = self.read_raw_data(ACCEL_XOUT_H + 2) / 16384.0
        az = self.read_raw_data(ACCEL_XOUT_H + 4) / 16384.0
        return (ax, ay, az)
    
    def get_gyro(self):
        gx = self.read_raw_data(GYRO_XOUT_H) / 131.0
        gy = self.read_raw_data(GYRO_XOUT_H + 2) / 131.0
        gz = self.read_raw_data(GYRO_XOUT_H + 4) / 131.0
        return (gx, gy, gz)

class SensorController:
    def __init__(self):
        self.mpu = MPU6050()
        self.vl53l0x = None
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.vl53l0x = adafruit_vl53l0x.VL53L0X(i2c)
            print("[SensorController] VL53L0X distance sensor initialized.")
        except Exception as e:
            print(f"[SensorController] VL53L0X init failed: {e}")
    
    def initialize_sensors(self):
        print("[SensorController] Sensors initialized.")
    
    def get_orientation(self):
        """Return accelerometer and gyro data"""
        accel = self.mpu.get_acceleration()
        gyro = self.mpu.get_gyro()
        return {'acceleration': accel, 'gyro': gyro}
    
    def get_distance(self):
        """Return distance from VL53L0X in mm, or None if sensor unavailable"""
        if self.vl53l0x:
            try:
                distance = self.vl53l0x.range
                return distance
            except Exception as e:
                print(f"[SensorController] Distance read error: {e}")
                return None
        else:
            return None
    
    def obstacle_detected(self, threshold_mm=200):
        """Returns True if obstacle is closer than threshold"""
        dist = self.get_distance()
        if dist is not None and dist < threshold_mm:
            print(f"[SensorController] Obstacle detected at {dist}mm")
            return True
        return False
    
    def is_tilted(self, tilt_threshold=0.3):
        """
        Detect if robot is tilted by checking acceleration vector deviation from gravity.
        tilt_threshold: allowable deviation from 1G acceleration in any axis.
        """
        ax, ay, az = self.mpu.get_acceleration()
        # Simple magnitude check, expecting ~1G (9.8 m/s² normalized)
        magnitude = (ax**2 + ay**2 + az**2) ** 0.5
        if abs(magnitude - 1) > tilt_threshold:
            print(f"[SensorController] Tilt detected! Acc magnitude: {magnitude:.2f}G")
            return True
        return False
