"""
GPIO interface service
"""
import logging
from typing import Iterable
import RPi.GPIO as GPIO
import adafruit_matrixkeypad as Keypad
logger = logging.getLogger(__name__)

ROWS=2
COLS=2
keys = ((1, 2),(3, 4))
rowsPins=[21,20]
colsPins=[16,12]


class GpioButtonMatrixInterface:
    """Service class for RPI Button Matrix GPIO"""

    rowsPins: Iterable[int]
    colsPins: Iterable[int]
    keypad: Keypad.Matrix_Keypad

    def __init__(self, rowsPins: Iterable[int], colsPins: Iterable[int]):

        logger.info(f"Creating RPI GPIO Button Matrix interface:")
        logger.info(f"rowsPins: {rowsPins}   colsPins: {colsPins}")

        self.rowsPins = rowsPins
        self.colsPins = colsPins

        # button matrix setup
        self.keypad = Keypad.Matrix_Keypad(rowsPins, colsPins, keys)


    def check_button_pressed(self):
        """Return the key of the button pressed, if not button"""
        logger.info("Checking if button is pressed")
        keys = self.keypad.pressed_keys
        if keys:
            logger.info(f"Buttons pressed: {keys}")
            return keys
        return None



