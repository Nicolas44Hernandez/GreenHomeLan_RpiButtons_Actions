"""
Pijuice battery interface service
"""
import logging
import time
from pijuice import PiJuice

logger = logging.getLogger(__name__)


class BatteryInterface:
    """Service class for Pijuice Battery management"""

    pijuice_battery: PiJuice

    def __init__(self):

        logger.info(f"Creating Pijuice Battery interface:")
        self.pijuice_battery = PiJuice(1, 0x14) # Instantiate PiJuice interface object

    def get_battery_level(self)-> int:
        """Returns pijuice battery level"""
        bat_level = self.pijuice_battery.status.GetChargeLevel()["data"]
        logger.info(f"Battery level: {bat_level}")
        return int(bat_level)

    def set_led_to_blink(self):
        """Set led to blink for 1 sec"""
        logger.info(f"Setting led to blink")
        self.pijuice_battery.status.SetLedBlink('D2', 5, [0,255,100], 20, [100, 0, 0], 50)
        time.sleep(1)
        self.pijuice_battery.status.SetLedState("D2", [0, 0, 0])
