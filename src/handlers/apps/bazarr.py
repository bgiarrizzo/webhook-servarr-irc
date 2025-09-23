from datetime import datetime
from typing import Dict, Callable

from handlers.events import events_handler
from irc.connection import IrcConnection

APP_NAME = "Bazarr"


class BazarrEventHandler:
    def __init__(self):
        self.event_map = {
            "info": self.on_info,
            "success": self.on_success,
            "error": self.on_error,
            "warning": self.on_warning,
        }

    def send_message_to_event_handler(self, event_type: str, irc: IrcConnection, message: str):
        message = f"[{APP_NAME}] {message}"
        events_handler.handle_event(event_type, irc, message)

    def handle_event(self, irc: IrcConnection, event_type: str, data: Dict):
        event_type = event_type.lower()
        handler = self.event_map.get(event_type, self.unknown_event)
        handler(irc, data)

    def unknown_event(self, irc: IrcConnection, data: Dict):
        message = f"Unknown event type: {data.get('type', 'Unknown')} - Payload = {data}"
        irc.send_message(message)

    def on_info(self, irc: IrcConnection, data: Dict):
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Test message from {APP_NAME} posted at {date_now}: {data.get('message', 'Unknown')}"
        self.send_message_to_event_handler(irc=irc, event_type="info", message=message)

    def on_success(self, irc: IrcConnection, data: Dict):
        message = data.get("message", "Unknown")
        self.send_message_to_event_handler(irc=irc, event_type="success", message=message)

    def on_error(self, irc: IrcConnection, data: Dict):
        message = data.get("message", "Unknown")
        self.send_message_to_event_handler(irc=irc, event_type="error", message=message)

    def on_warning(self, irc: IrcConnection, data: Dict):
        message = data.get("message", "Unknown")
        self.send_message_to_event_handler(irc=irc, event_type="warning", message=message)

    


bazarr = BazarrEventHandler()
