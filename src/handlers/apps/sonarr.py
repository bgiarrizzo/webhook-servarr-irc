from datetime import datetime
from typing import Dict

from handlers.events import events_handler
from irc.connection import IrcConnection

APP_NAME = "Sonarr"


class SonarrEventHandler:
    def __init__(self):
        self.event_map = {
            "applicationupdate": self.on_application_update,
            "download": self.on_download,
            "episodeadded": self.on_episode_added,
            "episodedelete": self.on_episode_deleted,
            "episodedeletedforupgrade": self.on_episode_deleted_for_upgrade,
            "episodefiledelete": self.on_episode_file_deleted,
            "episodeimported": self.on_episode_imported,
            "grab": self.on_grab,
            "health": self.on_health,
            "healthrestored": self.on_health_restored,
            "manualinteractionrequired": self.on_manual_interaction_required,
            "seriesdelete": self.on_series_delete,
            "renamed": self.on_rename,
            "test": self.on_test,
            "upgraded": self.on_upgrade,
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

    def on_episode_added(self, irc: IrcConnection, data: Dict):
        episode_name = data.get("episodes", {})[0].get("title", "Unknown")
        episode_number = data.get("episodes", {})[0].get("episodeNumber", "Unknown")
        season_number = data.get("episodes", {})[0].get("seasonNumber", "Unknown")
        series_name = data.get("series", {}).get("title", "Unknown")

        message = f"Added : {series_name} : S{season_number}E{episode_number} - {episode_name}"
        self.send_message_to_event_handler("added", irc, message)

    def on_application_update(self, irc: IrcConnection, data: Dict):
        previous_version = data.get("previousVersion", "Unknown")
        new_version = data.get("newVersion", "Unknown")

        message = f"Sonarr has been updated to version {new_version} from version {previous_version}"
        self.send_message_to_event_handler("application_update", irc, message)

    def on_download(self, irc: IrcConnection, data: Dict):
        series_name = data.get("series", {}).get("title", "Unknown")
        release_title = data.get("release", {}).get("releaseTitle", "Unknown")
        episode_list = (
            [
                episode.get("episodeNumber", "Unknown")
                for episode in data.get("episodes", [])
            ]
            if len(data.get("episodes", [])) > 1
            else [data.get("episodes", {})[0].get("episodeNumber", "Unknown")]
        )

        message = f"Download : Episodes {', '.join(episode_list)} - {series_name} - {release_title}"
        self.send_message_to_event_handler("download", irc, message)

    def on_episode_deleted(self, irc: IrcConnection, data: Dict):
        episode_name = data.get("episodes", {})[0].get("title", "Unknown")
        episode_number = data.get("episodes", {})[0].get("episodeNumber", "Unknown")
        season_number = data.get("episodes", {})[0].get("seasonNumber", "Unknown")
        series_name = data.get("series", {}).get("title", "Unknown")

        message = f"Deleted : {series_name} : S{season_number}E{episode_number} - {episode_name}"
        self.send_message_to_event_handler("file_deleted", irc, message)

    def on_episode_deleted_for_upgrade(self, irc: IrcConnection, data: Dict):
        episode_name = data.get("episodes", {})[0].get("title", "Unknown")
        file_name = data.get("episodeFile", {}).get("relativePath", "Unknown")

        message = f"Deleted for upgrade : {episode_name} - {file_name}"
        self.send_message_to_event_handler("file_deleted_for_upgrade", irc, message)

    def on_episode_file_deleted(self, irc: IrcConnection, data: Dict):
        episode_name = data.get("episodes", {})[0].get("title", "Unknown")
        episode_number = data.get("episodes", {})[0].get("episodeNumber", "Unknown")
        season_number = data.get("episodes", {})[0].get("seasonNumber", "Unknown")
        series_name = data.get("series", {}).get("title", "Unknown")
        file_name = data.get("episodeFile", {}).get("relativePath", "Unknown")

        message = f"Episode File deleted : {series_name} : S{season_number}E{episode_number} - {episode_name} - {file_name}"
        self.send_message_to_event_handler("episode_file_deleted", irc, message)

    def on_episode_imported(self, irc: IrcConnection, data: Dict):
        episode_name = data.get("episodes", {})[0].get("title", "Unknown")
        episode_number = data.get("episodes", {})[0].get("episodeNumber", "Unknown")
        season_number = data.get("episodes", {})[0].get("seasonNumber", "Unknown")
        series_name = data.get("series", {}).get("title", "Unknown")

        message = f"Imported : {series_name} : S{season_number}E{episode_number} - {episode_name}"
        self.send_message_to_event_handler("import", irc, message)

    def on_rename(self, irc: IrcConnection, data: Dict):
        old_file_name = data.get("oldPath", "Unknown")
        new_file_name = data.get("newPath", "Unknown")

        message = f"Renamed : {old_file_name} to {new_file_name}"
        self.send_message_to_event_handler("rename", irc, message)

    def on_grab(self, irc: IrcConnection, data: Dict):
        episode_name = data.get("episodes", {})[0].get("title", "Unknown")
        series_name = data.get("series", {}).get("title", "Unknown")
        release_title = data.get("release", {}).get("releaseTitle", "Unknown")
        quality = data.get("release", {}).get("quality", "Unknown")
        size_in_gigabytes = data.get("release", {}).get("size", 0) / 1024 / 1024 / 1024
        size_in_gigabytes = f"{round(size_in_gigabytes, 2)} GB"

        message = (
            f"Grabbed : {episode_name} from {series_name} - ReleaseTitle = {release_title} - "
            f"{quality} - Size = {size_in_gigabytes}"
        )
        self.send_message_to_event_handler("grab", irc, message)

    def on_health(self, irc: IrcConnection, data: Dict):
        issue_type = data.get("type", "Unknown")
        issue_message = data.get("message", "No message")

        message = f"Sonarr health check issue - {issue_type} : {issue_message}"
        self.send_message_to_event_handler("health", irc, message)

    def on_health_restored(self, irc: IrcConnection, data: Dict):
        issue_type = data.get("type", "Unknown")
        issue_message = data.get("message", "No message")

        message = f"Sonarr health check restored - {issue_type} : {issue_message}"
        self.send_message_to_event_handler("health_restored", irc, message)

    def on_manual_interaction_required(self, irc: IrcConnection, data: Dict):
        message = f"Manual interaction required: {data.get('message', 'No message')}"
        self.send_message_to_event_handler("manual_interaction_required", irc, message)

    def on_series_delete(self, irc: IrcConnection, data: Dict):
        series_name = data.get("series", {}).get("title", "Unknown")

        message = f"Series deleted: {series_name}"
        self.send_message_to_event_handler("series_deleted", irc, message)

    def on_test(self, irc: IrcConnection, data: Dict):
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message = f"Test message from {APP_NAME} posted at {date_now}"
        self.send_message_to_event_handler("test", irc, message)

    def on_upgrade(self, irc: IrcConnection, data: Dict):
        episode_name = data.get("episodes", {})[0].get("title", "Unknown")

        message = f"Upgraded : {episode_name}"
        self.send_message_to_event_handler("upgrade", irc, message)


sonarr = SonarrEventHandler()
