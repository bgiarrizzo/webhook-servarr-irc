from typing import Dict
from irc.connection import IrcConnection

from .radarr import radarr
from .bazarr import bazarr
from .sonarr import sonarr
from .lidarr import lidarr
from .readarr import readarr
from .prowlarr import prowlarr


def handle_app(irc: IrcConnection, app_name: str, event_type: str, data: Dict):
    app_name = app_name.lower()

    if app_name == "radarr":
        radarr.handle_event(irc, event_type, data)
    elif app_name == "bazarr":
        bazarr.handle_event(irc, event_type, data)
    elif app_name == "sonarr":
        sonarr.handle_event(irc, event_type,data)
    elif app_name == "lidarr":
        lidarr.handle_event(irc, event_type,data)
    elif app_name == "readarr":
        readarr.handle_event(irc, event_type,data)
    elif app_name == "prowlarr":
        prowlarr.handle_event(irc, event_type, data)
    else:
        message = f"Event {event_type} for unknown app {app_name}: {data}"
        irc.send_message(message)
