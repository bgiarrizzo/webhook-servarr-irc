from datetime import datetime
from typing import Dict

from handlers.events import events_handler
from irc.connection import IrcConnection

APP_NAME = "Radarr"

class RadarrEventHandler:
    def __init__(self):
        self.event_map = {
            "test": self.on_test,
            "grab": self.on_grab,
            "movieimported": self.on_import,
            "upgrade": self.on_upgrade,
            "rename": self.on_rename,
            "movieadded": self.on_added,
            "moviedelete": self.on_deleted,
            "moviedeletedforupgrade": self.on_deleted_for_upgrade,
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
        movie_name = data.get("movie", {}).get("title", "Unknown")
        indexer_name = data.get("release", {}).get("indexer", "Unknown")
        release_title = data.get("release", {}).get("releaseTitle", "Unknown")
        quality = data.get("release", {}).get("quality", "Unknown")
        size_in_gigabytes = data.get("release", {}).get("size", 0) / 1024 / 1024 / 1024
        size_in_gigabytes = f"{round(size_in_gigabytes, 2)} GB"

        message = (
            f"Grabbed : {movie_name} from {indexer_name} - ReleaseTitle = {release_title} - "
            f"{quality} - Size = {size_in_gigabytes}"
        )
        self.send_message_to_event_handler("grab", irc, message)

    def on_import(self, irc: IrcConnection, data: Dict):
        movie_name = data.get("movie", {}).get("title", "Unknown")
        message = f"Imported : {movie_name}"
        self.send_message_to_event_handler("import", irc, message)

    def on_upgrade(self, irc: IrcConnection, data: Dict):
        movie_name = data.get("movie", {}).get("title", "Unknown")
        message = f"Upgraded : {movie_name}"
        self.send_message_to_event_handler("upgrade", irc, message)

    def on_rename(self, irc: IrcConnection, data: Dict):
        old_file_name = data.get("oldPath", "Unknown")
        new_file_name = data.get("newPath", "Unknown")
        message = f"Renamed : {old_file_name} to {new_file_name}"
        self.send_message_to_event_handler("rename", irc, message)

    def on_added(self, irc: IrcConnection, data: Dict):
        movie_name = data.get("movie", {}).get("title", "Unknown")
        movie_year = data.get("movie", {}).get("year", "Unknown")
        tmdb_movie_id = data.get("movie", {}).get("tmdbId", "Unknown")
        movie_tmdb_url = f"https://www.themoviedb.org/movie/{tmdb_movie_id}"
        message = f"Added : {movie_name} - {movie_year} - {movie_tmdb_url}"
        self.send_message_to_event_handler("added", irc, message)

    def on_deleted(self, irc: IrcConnection, data: Dict):
        movie_name = data.get("movie", {}).get("title", "Unknown")
        message = f"Deleted : {movie_name}"
        self.send_message_to_event_handler("file_deleted", irc, message)

    def on_deleted_for_upgrade(self, irc: IrcConnection, data: Dict):
        movie_name = data.get("movie", {}).get("title", "Unknown")
        file_name = data.get("movieFile", {}).get("relativePath", "Unknown")
        message = f"Deleted for upgrade : {movie_name} - {file_name}"
        self.send_message_to_event_handler("file_deleted_for_upgrade", irc, message)

    def on_health_issue(self, irc: IrcConnection, data: Dict):
        issue_type = data.get("type", "Unknown")
        issue_message = data.get("message", "No message")
        message = f"Radarr health check issue - {issue_type} : {issue_message}"
        self.send_message_to_event_handler("health_issue", irc, message)

    def on_health_restored(self, irc: IrcConnection, data: Dict):
        issue_type = data.get("type", "Unknown")
        issue_message = data.get("message", "No message")
        message = f"Radarr health check restored - {issue_type} : {issue_message}"
        self.send_message_to_event_handler("health_restored", irc, message)

    def on_application_update(self, irc: IrcConnection, data: Dict):
        previous_version = data.get("previousVersion", "Unknown")
        new_version = data.get("version", "Unknown")
        message = f"Radarr has been updated to version {new_version} from version {previous_version}"
        self.send_message_to_event_handler("application_update", irc, message)

    def on_manual_interaction_required(self, irc: IrcConnection, data: Dict):
        message = f"Manual interaction required: {data.get('message', 'No message')}"
        self.send_message_to_event_handler("manual_interaction_required", irc, message)    

radarr = RadarrEventHandler()
