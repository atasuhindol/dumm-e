"""
display_controller.py

Controls SSD1106 OLED display.
Shows eye animations and simple text messages.
"""

import time
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106  # Note: use sh1106 if SSD1306 driver unavailable; adjust if needed
from PIL import Image, ImageDraw, ImageFont
import os

class DisplayController:
    def __init__(self):
        # Initialize I2C interface and OLED device
        serial = i2c(port=1, address=0x3C)
        self.device = sh1106(serial)  # or SSD1306 if your display is that
        self.width = self.device.width
        self.height = self.device.height
        self.font = ImageFont.load_default()
        self.assets_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'eyes')
        self.current_image = None
    
    def init_display(self):
        self.device.clear()
        self.show_message("Robot Ready")
    
    def clear_display(self):
        self.device.clear()
    
    def show_message(self, message, duration=2):
        img = Image.new('1', (self.width, self.height), "black")
        draw = ImageDraw.Draw(img)
        w, h = draw.textsize(message, font=self.font)
        draw.text(((self.width - w) // 2, (self.height - h) // 2), message, font=self.font, fill=255)
        self.device.display(img)
        time.sleep(duration)
        self.clear_display()
    
    def show_eyes(self, expression="neutral"):
        """
        Display eye animation based on expression.
        Expressions: neutral, happy, sad, surprised, closed
        """
        filename = f"{expression}.bmp"
        filepath = os.path.join(self.assets_path, filename)
        if not os.path.isfile(filepath):
            print(f"[DisplayController] Eye image not found: {filepath}")
            return
        
        try:
            img = Image.open(filepath).resize((self.width, self.height)).convert('1')
            self.device.display(img)
            self.current_image = img
        except Exception as e:
            print(f"[DisplayController] Failed to load eye image: {e}")
    
    def blink_eyes(self, interval=0.3):
        self.show_eyes("closed")
        time.sleep(interval)
        self.show_eyes("neutral")
