"""
i2c_tools.py

Utility functions for scanning and initializing I2C devices.
Useful for debugging and confirming connected I2C addresses.
"""

import smbus2

def scan_i2c(bus_number=1):
    """
    Scan the I2C bus for connected devices.
    :param bus_number: I2C bus number, typically 1 on Raspberry Pi
    :return: List of detected device addresses
    """
    bus = smbus2.SMBus(bus_number)
    devices = []
    print("Scanning I2C bus...")
    for address in range(0x03, 0x78):
        try:
            bus.read_byte(address)
            devices.append(address)
            print(f"Found device at 0x{address:02X}")
        except OSError:
            # No device at this address
            pass
    bus.close()
    if not devices:
        print("No I2C devices found.")
    return devices

def initialize_device(bus_number=1, address=0x00, init_commands=None):
    """
    Send initialization commands to I2C device.
    :param bus_number: I2C bus number
    :param address: I2C device address
    :param init_commands: list of (register, value) tuples
    """
    if init_commands is None:
        init_commands = []
    bus = smbus2.SMBus(bus_number)
    try:
        for reg, val in init_commands:
            bus.write_byte_data(address, reg, val)
            print(f"Sent init command to 0x{address:02X}: reg=0x{reg:02X}, val=0x{val:02X}")
    except Exception as e:
        print(f"Error initializing device at 0x{address:02X}: {e}")
    finally:
        bus.close()
