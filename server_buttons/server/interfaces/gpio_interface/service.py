"""
GPIO interface service
"""
import logging
import time
from gpiozero import DigitalOutputDevice, DigitalInputDevice

logger = logging.getLogger(__name__)

KEYS = [1, 2, 3, 4]

class GpioButtonMatrixInterface:
    """Service class for RPI Button Matrix GPIO"""

    row_1: DigitalOutputDevice
    row_2: DigitalOutputDevice
    col_1: DigitalInputDevice
    col_2: DigitalInputDevice
    def __init__(self, row_1_pin: int, row_2_pin: int, col_1_pin: int, col_2_pin: int):

        logger.info(f"Creating RPI GPIO Button Matrix interface:")
        logger.info(f"row_1_pin: {row_1_pin}  row_2_pin: {row_2_pin} - col_1_pin: {col_1_pin}  col_2_pin: {col_2_pin}   ")

        self.row_1 = DigitalOutputDevice(pin=row_1_pin, active_high=True)
        self.row_2 = DigitalOutputDevice(pin=row_2_pin,active_high=True)
        self.col_1 = DigitalInputDevice(pin=col_1_pin)
        self.col_2 = DigitalInputDevice(pin=col_2_pin)

    def check_button_pressed(self):
        """Return the key of the button pressed, if not button"""

        # Set row_1 to high and row_2 to low
        self.row_1.on()
        self.row_2.off()
        time.sleep(5/1000)

        # Check output values
        if self.col_1.value:
            return KEYS[0]
        if self.col_2.value:
            return KEYS[1]

        # Set row_1 to low and row_2 to high
        self.row_1.off()
        self.row_2.on()
        time.sleep(5/1000)

        # Check output values
        if self.col_1.value:
            return KEYS[2]
        if self.col_2.value:
            return KEYS[3]

        # Return None any button pressed
        return None



