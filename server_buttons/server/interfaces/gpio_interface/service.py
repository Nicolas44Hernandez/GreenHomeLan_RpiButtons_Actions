"""
GPIO interface service
"""
import logging
from typing import Iterable
import RPi.GPIO as GPIO
import Keypad

logger = logging.getLogger(__name__)

ROWS=2
COLS=2
keys = ["1","2","3", "4"]

rowsPins=[21,20]
colsPins=[16,12]


class GpioButtonMatrixInterface:
    """Service class for RPI Button Matrix GPIO"""

    rowsPins: Iterable[int]
    colsPins: Iterable[int]
    keypad: Keypad.Keypad

    def __init__(self, rowsPins: Iterable[int], colsPins: Iterable[int]):

        logger.info(f"Creating RPI GPIO Button Matrix interface:")
        logger.info(f"rowsPins: {rowsPins}   colsPins: {colsPins}")

        self.rowsPins = rowsPins
        self.colsPins = colsPins

        # button matrix setup
        self.keypad = Keypad.Keypad(keys, rowsPins, colsPins, ROWS, COLS)
        self.keypad.setDebounceTime(50)


    def check_button_pressed(self):
        """Return the key of the button pressed, if not button"""
        logger.info("Checking if button is pressed")
        key = self.keypad.getKey()
        if key != self.keypad.NULL:
            logger.info(f"Button pressed: {key}")
            return key
        return None



