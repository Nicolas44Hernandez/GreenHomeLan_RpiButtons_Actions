import logging
from server.managers.thread_manager import thread_manager_service
from flask import Flask

logger = logging.getLogger(__name__)


class CommandSender:
    """Manager for CommandSender"""

    mqtt_commands_topic: str

    def __init__(self, app: Flask = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Initialize CommandSender"""
        if app is not None:
            logger.info("initializing the CommandsSender")
            self.mqtt_commands_topic = app.config["MQTT_ORCHESTRATOR_COMMANDS_TOPIC"]

    def send_command_to_orchestrator(self, command: str):
        """Notify alarm to orchestrator"""

        logger.info(f"Sending command via Thread")
        return thread_manager_service.send_thread_message_to_border_router(command)


commands_sender_service: CommandSender = CommandSender()
""" CommandSender service singleton"""
