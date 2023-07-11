import logging
from timeloop import Timeloop
from flask import Flask
from server.interfaces.gpio_interface import GpioButtonMatrixInterface
#from server.notification import notification_service

logger = logging.getLogger(__name__)


class ButtonsMatrixManager:
    """Manager for Buttons matrix peripheral"""

    gpio_interface: GpioButtonMatrixInterface
    therad_messages = {}

    def __init__(self, app: Flask = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Initialize ButtonManager"""
        if app is not None:
            logger.info("initializing the ButtonsMatrixManager")

            self.gpio_interface = GpioButtonMatrixInterface(
                rowsPins=[
                    app.config["PERIPHERALS_BUTTONS_MATRIX_L1"],
                    app.config["PERIPHERALS_BUTTONS_MATRIX_L2"],
                ],
                colsPins=[
                    app.config["PERIPHERALS_BUTTONS_MATRIX_C1"],
                    app.config["PERIPHERALS_BUTTONS_MATRIX_C2"],
                ],
            )


    def button_press_callback(self, key):
        """Callback function for button press"""
        logger.info(f"Button {key} pressed")

        # Notify the alarm to orchestrator
        #notification_service.notify_alarm(alarm_type="emergency_btn", msg="button pressed")

buttons_matrix_manager_service: ButtonsMatrixManager = ButtonsMatrixManager()
""" Buttons matrix manager service singleton"""
