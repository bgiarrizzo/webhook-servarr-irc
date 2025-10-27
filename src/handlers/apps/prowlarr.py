from datetime import datetime
from typing import Dict

from handlers.events import events_handler
from irc.connection import IrcConnection

APP_NAME = "Prowlarr"


class ProwlarrEventHandler:
    def __init__(self):
        self.event_map = {
            "applicationupdate": self.on_application_update,
            "grab": self.on_grab,
            "health": self.on_health_issue,
            "healthrestored": self.on_health_restored,
            "indexeradded": self.on_indexer_added,
            "indexererror": self.on_indexer_error,
            "indexerremoved": self.on_indexer_removed,
            "indexerupdated": self.on_indexer_updated,
            "manualinteractionrequired": self.on_manual_interaction_required,
            "test": self.on_test,
        }

    def send_message_to_event_handler(
        self, event_type: str, irc: IrcConnection, message: str
    ):
        message = f"[{APP_NAME}] {message}"
        events_handler.handle_event(event_type, irc, message)

    def handle_event(self, irc: IrcConnection, event_type: str, data: Dict):
        event_type = event_type.lower()
        handler = self.event_map.get(event_type, self.unknown_event)
        handler(irc, data)

    def unknown_event(self, irc: IrcConnection, data: Dict):
        message = (
            f"Unknown event type: {data.get('eventType', 'Unknown')} - Payload = {data}"
        )
        self.send_message_to_event_handler("error", irc, message)

    def on_application_update(self, irc: IrcConnection, data: Dict):
        previous_version = data.get("previousVersion", "Unknown")
        new_version = data.get("newVersion", "Unknown")

        message = f"Prowlarr has been updated to version {new_version} from version {previous_version}"
        self.send_message_to_event_handler("application_update", irc, message)

    def on_grab(self, irc: IrcConnection, data: Dict):
        release_title = data.get("release", {}).get("releaseTitle", "Unknown")
        indexer_name = data.get("release", {}).get("indexer", "Unknown")
        source = data.get("source", "Unknown")

        message = (
            f"Grabbed : {release_title} from {indexer_name}, requested by {source}"
        )
        self.send_message_to_event_handler("grab", irc, message)

    def on_health_issue(self, irc: IrcConnection, data: Dict):
        issue_type = data.get("type", "Unknown")
        issue_message = data.get("message", "No message")

        message = f"Prowlarr health check issue - {issue_type} : {issue_message}"
        self.send_message_to_event_handler("health", irc, message)

    def on_health_restored(self, irc: IrcConnection, data: Dict):
        issue_type = data.get("type", "Unknown")
        issue_message = data.get("message", "No message")

        message = f"Prowlarr health check restored - {issue_type} : {issue_message}"
        self.send_message_to_event_handler("health_restored", irc, message)

    def on_indexer_added(self, irc: IrcConnection, data: Dict):
        indexer_name = data.get("indexer", {}).get("name", "Unknown")

        message = f"Indexer added: {indexer_name}"
        self.send_message_to_event_handler("info", irc, message)

    def on_indexer_error(self, irc: IrcConnection, data: Dict):
        indexer_name = data.get("indexer", {}).get("name", "Unknown")
        error_message = data.get("message", "No message")

        message = f"Indexer error: {indexer_name} - {error_message}"
        self.send_message_to_event_handler("error", irc, message)

    def on_indexer_removed(self, irc: IrcConnection, data: Dict):
        indexer_name = data.get("indexer", {}).get("name", "Unknown")

        message = f"Indexer removed: {indexer_name}"
        self.send_message_to_event_handler("info", irc, message)

    def on_indexer_updated(self, irc: IrcConnection, data: Dict):
        indexer_name = data.get("indexer", {}).get("name", "Unknown")

        message = f"Indexer updated: {indexer_name}"
        self.send_message_to_event_handler("info", irc, message)

    def on_manual_interaction_required(self, irc: IrcConnection, data: Dict):
        message = f"Manual interaction required: {data.get('message', 'No message')}"
        self.send_message_to_event_handler("manual_interaction_required", irc, message)

    def on_test(self, irc: IrcConnection, data: Dict):
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message = f"Test message from {APP_NAME} posted at {date_now}"
        self.send_message_to_event_handler("test", irc, message)


prowlarr = ProwlarrEventHandler()
