import logging
from datetime import timedelta
from timeloop import Timeloop
from flask import Flask
from server.interfaces.gpio_interface import GpioButtonMatrixInterface
from server.commands_sender import commands_sender_service

logger = logging.getLogger(__name__)

buttons_status_timeloop = Timeloop()

class ButtonsMatrixManager:
    """Manager for Buttons matrix peripheral"""

    gpio_interface: GpioButtonMatrixInterface
    therad_messages = {}
    buttons_polling_period_in_ms: int

    def __init__(self, app: Flask = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Initialize ButtonManager"""
        if app is not None:
            logger.info("initializing the ButtonsMatrixManager")

            self.gpio_interface = GpioButtonMatrixInterface(
                row_1_pin=app.config["PERIPHERALS_BUTTONS_MATRIX_L1"],
                row_2_pin=app.config["PERIPHERALS_BUTTONS_MATRIX_L2"],
                col_1_pin=app.config["PERIPHERALS_BUTTONS_MATRIX_C1"],
                col_2_pin=app.config["PERIPHERALS_BUTTONS_MATRIX_C2"],
            )
            self.buttons_polling_period_in_ms = app.config["BUTTONS_STATUS_POLL_PERIOD_IN_MS"]

            # Set polling task
            self.schedule_buttons_status_polling()

    def schedule_buttons_status_polling(self):
        """Schedule the buttons status polling"""

        # Buttons status polling job
        @buttons_status_timeloop.job(interval=timedelta(milliseconds=self.buttons_polling_period_in_ms))
        def check_buttons_pressed():
            #logger.info(f"Launch buttons status polling")
            pressed = self.gpio_interface.check_button_pressed()
            if pressed is not None:
                self.button_press_callback(pressed)

        buttons_status_timeloop.start(block=False)


    def button_press_callback(self, key: int):
        """Callback function for button press"""
        logger.info(f"Button pressed {key}")
        # Send the command to orchestrator
        cmd = f"cmd_{key}"
        commands_sender_service.send_command_to_orchestrator(command=cmd)

buttons_matrix_manager_service: ButtonsMatrixManager = ButtonsMatrixManager()
""" Buttons matrix manager service singleton"""
