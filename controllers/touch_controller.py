"""
touch_controller.py

Handles input from TTP223B capacitive touch sensor.
Uses Raspberry Pi GPIO to detect touch events and trigger callbacks.
"""

import RPi.GPIO as GPIO
import threading
import time

class TouchController:
    def __init__(self, touch_pin=17):
        """
        :param touch_pin: GPIO pin connected to TTP223B output
        """
        self.touch_pin = touch_pin
        self.callback = None
        self.running = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.touch_pin, GPIO.IN)
    
    def start_listening(self, callback):
        """
        Start listening for touch events.
        :param callback: function to call on touch event (no params)
        """
        self.callback = callback
        self.running = True
        GPIO.add_event_detect(self.touch_pin, GPIO.RISING, callback=self._handle_touch, bouncetime=200)
        print("[TouchController] Started listening for touch events.")
    
    def _handle_touch(self, channel):
        print("[TouchController] Touch detected!")
        if self.callback:
            self.callback()
    
    def stop_listening(self):
        """
        Stop listening and clean up GPIO event detection.
        """
        if self.running:
            GPIO.remove_event_detect(self.touch_pin)
            self.running = False
            print("[TouchController] Stopped listening.")
    
    def cleanup(self):
        self.stop_listening()
        GPIO.cleanup()
        print("[TouchController] GPIO cleaned up.")
