"""
motor_controller.py

Controls two DC motors via MX1508 motor driver.
Provides simple forward, backward, left, right and stop functions.
"""

import RPi.GPIO as GPIO
import time

class MotorController:
    def __init__(self, motor1_pins=(17, 18), motor2_pins=(22, 23), pwm_freq=1000):
        """
        :param motor1_pins: tuple(GPIO_pin_forward, GPIO_pin_backward) for motor 1
        :param motor2_pins: tuple(GPIO_pin_forward, GPIO_pin_backward) for motor 2
        :param pwm_freq: PWM frequency in Hz
        """
        self.motor1_forward_pin, self.motor1_backward_pin = motor1_pins
        self.motor2_forward_pin, self.motor2_backward_pin = motor2_pins
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor1_forward_pin, GPIO.OUT)
        GPIO.setup(self.motor1_backward_pin, GPIO.OUT)
        GPIO.setup(self.motor2_forward_pin, GPIO.OUT)
        GPIO.setup(self.motor2_backward_pin, GPIO.OUT)
        
        # Set up PWM for speed control
        self.motor1_forward_pwm = GPIO.PWM(self.motor1_forward_pin, pwm_freq)
        self.motor1_backward_pwm = GPIO.PWM(self.motor1_backward_pin, pwm_freq)
        self.motor2_forward_pwm = GPIO.PWM(self.motor2_forward_pin, pwm_freq)
        self.motor2_backward_pwm = GPIO.PWM(self.motor2_backward_pin, pwm_freq)
        
        self.motor1_forward_pwm.start(0)
        self.motor1_backward_pwm.start(0)
        self.motor2_forward_pwm.start(0)
        self.motor2_backward_pwm.start(0)
    
    def _set_motor(self, forward_pwm, backward_pwm, speed):
        """
        Helper to set PWM signals for a single motor.
        :param speed: -100 to 100 (negative = backward)
        """
        speed = max(min(speed, 100), -100)  # Clamp speed
        if speed > 0:
            forward_pwm.ChangeDutyCycle(speed)
            backward_pwm.ChangeDutyCycle(0)
        elif speed < 0:
            forward_pwm.ChangeDutyCycle(0)
            backward_pwm.ChangeDutyCycle(-speed)
        else:
            forward_pwm.ChangeDutyCycle(0)
            backward_pwm.ChangeDutyCycle(0)
    
    def move(self, motor1_speed=0, motor2_speed=0):
        """Set speed for each motor"""
        self._set_motor(self.motor1_forward_pwm, self.motor1_backward_pwm, motor1_speed)
        self._set_motor(self.motor2_forward_pwm, self.motor2_backward_pwm, motor2_speed)
    
    def forward(self, speed=50):
        self.move(speed, speed)
    
    def backward(self, speed=50):
        self.move(-speed, -speed)
    
    def turn_left(self, speed=50):
        self.move(-speed, speed)
    
    def turn_right(self, speed=50):
        self.move(speed, -speed)
    
    def stop(self):
        self.move(0, 0)
    
    def cleanup(self):
        self.stop()
        self.motor1_forward_pwm.stop()
        self.motor1_backward_pwm.stop()
        self.motor2_forward_pwm.stop()
        self.motor2_backward_pwm.stop()
        GPIO.cleanup()
        print("[MotorController] Motors stopped and GPIO cleaned up.")
