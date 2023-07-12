import logging
from server.managers.mqtt_manager import mqtt_manager_service
from server.managers.thread_manager import thread_manager_service
from server.managers.wifi_connection_manager import wifi_connection_manager_service
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

        logger.info(f"Sending command to orchestrator:{command}")
        if wifi_connection_manager_service.connected:
            return self.send_command_via_mqtt(command=command)
        else:
            return self.send_command_via_thread(command=command)

    def send_command_via_mqtt(self, command: str) -> bool:
        """Send command via MQTT message"""
        logger.info(f"Sending command via MQTT")

        data = {"command": command}

        if mqtt_manager_service.publish_message(topic=self.mqtt_commands_topic, message=data):
            logger.info(f"Command {data} published to MQTT topic {self.mqtt_commands_topic}")
            return True
        else:
            logger.error(f"Impossible to publish command to MQTT topic {self.mqtt_commands_topic}")
            return False

    def send_command_via_thread(self, command: str) -> bool:
        """Send command via Thread message"""
        logger.info(f"Sending command via Thread")
        return thread_manager_service.send_thread_message_to_border_router(command)


commands_sender_service: CommandSender = CommandSender()
""" CommandSender service singleton"""
