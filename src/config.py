from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Attributes of the server this bot will run on
    SERVER_HOST: str = ""
    SERVER_PORT: int = 8000

    # Attributes of the IRC connection
    IRC_SERVER: str = "irc.192.168.1.230.nip.io"
    IRC_PORT: int = 6667

    IRC_CHANNEL: str = "#cloe"
    IRC_NICK: str = "cloe"

    # Set the password for your registered empty, leave empty if not applicable
    # Note: freenode(and potentially other servers) want password to be of the form
    # "nick:pass", so for ex. IRC_PASS = 'WfTestBot:mypass123'
    IRC_PASS: str = "p4ssw0rd"


settings = Settings()
