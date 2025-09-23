from datetime import datetime
from typing import Dict

from handlers.events import events_handler
from irc.connection import IrcConnection

APP_NAME = "Readarr"

class ReadarrEventHandler:
    def __init__(self):
        self.event_map = {
            "test": self.on_test,
            "grab": self.on_grab,
            "release": self.on_release,
            "download": self.on_download,
            "rename": self.on_rename,
            "bookimport": self.on_book_import,
            "bookdelete": self.on_book_delete,
            "bookfiledelete": self.on_book_file_delete,
            "bookfiledeleteforupgrade": self.on_book_file_delete_for_upgrade,
            "authoradd": self.on_author_add,
            "authordelete": self.on_author_delete,
            "healthissue": self.on_health_issue,
            "healthrestored": self.on_health_restored,
            "applicationupdate": self.on_application_update,
            "manualinteractionrequired": self.on_manual_interaction_required,
        }

    def send_message_to_event_handler(self, event_type: str, irc: IrcConnection, message: str):
        message = f"[{APP_NAME}] {message}"
        events_handler.handle_event(event_type, irc, message)

    def handle_event(self, irc: IrcConnection, event_type: str, data: Dict):
        event_type = event_type.lower()
        handler = self.event_map.get(event_type, self.unknown_event)
        handler(irc, data)

    def unknown_event(self, irc: IrcConnection, data: Dict):
        message = f"Unknown event type: {data.get('eventType', 'Unknown')} - Payload = {data}"
        self.send_message_to_event_handler("error", irc, message)

    def on_test(self, irc: IrcConnection, data: Dict = None):
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Test message from {APP_NAME} posted at {date_now}"
        self.send_message_to_event_handler("test", irc, message)

    def on_grab(self, irc: IrcConnection, data: Dict):
        book_title = data.get("book", {}).get("title", "Unknown")
        author_name = data.get("author", {}).get("name", "Unknown")
        release_title = data.get("release", {}).get("releaseTitle", "Unknown")
        quality = data.get("release", {}).get("quality", "Unknown")
        size = data.get("release", {}).get("size", 0)
        size_str = f"{size / (1024*1024):.2f} MB" if size else "Unknown"

        message = f"Grabbed: {book_title} by {author_name} - Quality: {quality} - Size: {size_str}"
        self.send_message_to_event_handler("grab", irc, message)

    def on_release(self, irc: IrcConnection, data: Dict):
        book_title = data.get("book", {}).get("title", "Unknown")
        author_name = data.get("author", {}).get("name", "Unknown")
        message = f"Released: {book_title} by {author_name}"
        self.send_message_to_event_handler("info", irc, message)

    def on_download(self, irc: IrcConnection, data: Dict):
        book_title = data.get("book", {}).get("title", "Unknown")
        author_name = data.get("author", {}).get("name", "Unknown")
        message = f"Downloaded: {book_title} by {author_name}"
        self.send_message_to_event_handler("info", irc, message)

    def on_rename(self, irc: IrcConnection, data: Dict):
        author_name = data.get("author", {}).get("name", "Unknown")
        message = f"Renamed files for author: {author_name}"
        self.send_message_to_event_handler("rename", irc, message)

    def on_book_import(self, irc: IrcConnection, data: Dict):
        book_title = data.get("book", {}).get("title", "Unknown")
        author_name = data.get("author", {}).get("name", "Unknown")
        quality = data.get("bookFile", {}).get("quality", "Unknown")
        message = f"Imported: {book_title} by {author_name} - Quality: {quality}"
        self.send_message_to_event_handler("import", irc, message)

    def on_book_delete(self, irc: IrcConnection, data: Dict):
        book_title = data.get("book", {}).get("title", "Unknown")
        message = f"Book deleted: {book_title}"
        self.send_message_to_event_handler("file_deleted", irc, message)

    def on_book_file_delete(self, irc: IrcConnection, data: Dict):
        book_path = data.get("bookFile", {}).get("path", "Unknown")
        message = f"Book file deleted: {book_path}"
        self.send_message_to_event_handler("file_deleted", irc, message)

    def on_book_file_delete_for_upgrade(self, irc: IrcConnection, data: Dict):
        book_title = data.get("book", {}).get("title", "Unknown")
        old_quality = data.get("bookFile", {}).get("quality", "Unknown")
        message = f"Book file deleted for upgrade: {book_title} - Old quality: {old_quality}"
        self.send_message_to_event_handler("file_deleted_for_upgrade", irc, message)

    def on_author_add(self, irc: IrcConnection, data: Dict):
        author_name = data.get("author", {}).get("name", "Unknown")
        message = f"Author added: {author_name}"
        self.send_message_to_event_handler("added", irc, message)

    def on_author_delete(self, irc: IrcConnection, data: Dict):
        author_name = data.get("author", {}).get("name", "Unknown")
        message = f"Author deleted: {author_name}"
        self.send_message_to_event_handler("file_deleted", irc, message)

    def on_health_issue(self, irc: IrcConnection, data: Dict):
        issue_type = data.get("type", "Unknown")
        issue_message = data.get("message", "No message")
        message = f"Readarr health check issue - {issue_type}: {issue_message}"
        self.send_message_to_event_handler("health_issue", irc, message)

    def on_health_restored(self, irc: IrcConnection, data: Dict):
        issue_type = data.get("type", "Unknown")
        issue_message = data.get("message", "No message")
        message = f"Readarr health check restored - {issue_type}: {issue_message}"
        self.send_message_to_event_handler("health_restored", irc, message)

    def on_application_update(self, irc: IrcConnection, data: Dict):
        previous_version = data.get("previousVersion", "Unknown")
        new_version = data.get("newVersion", "Unknown")
        message = f"Readarr updated from version {previous_version} to {new_version}"
        self.send_message_to_event_handler("application_update", irc, message)

    def on_manual_interaction_required(self, irc: IrcConnection, data: Dict):
        message = f"Manual interaction required: {data.get('message', 'No message')}"
        self.send_message_to_event_handler("manual_interaction_required", irc, message)

readarr = ReadarrEventHandler()
