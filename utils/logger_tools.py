"""
logger.py

Basic logger utility to log messages with timestamps.
Supports different log levels: INFO, WARNING, ERROR.
"""

import logging
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "robot.log")

def setup_logger():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    logger = logging.getLogger("MiniRobotLogger")
    logger.setLevel(logging.DEBUG)
    
    # File handler for logging to a file
    fh = logging.FileHandler(LOG_FILE)
    fh.setLevel(logging.DEBUG)
    
    # Console handler for printing to stdout
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Log format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

logger = setup_logger()

# Example usage:
# logger.info("Robot started")
# logger.warning("Low battery")
# logger.error("Motor failure detected")
