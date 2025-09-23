import threading
from http.server import HTTPServer

from handlers.http import HTTPHandler
from irc.connection import IrcConnection
from config import settings

def irc_worker(irc):
    irc.loop()

irc = IrcConnection(
    server=settings.IRC_SERVER,
    channel=settings.IRC_CHANNEL,
    nick=settings.IRC_NICK,
    passw=settings.IRC_PASS,
    port=settings.IRC_PORT,
)

HTTPHandler.set_irc(irc)

irc_thread = threading.Thread(target=irc_worker, args=(irc,))
irc_thread.start()

try:
    server = HTTPServer((settings.SERVER_HOST, settings.SERVER_PORT), HTTPHandler)
    print(f"Server started on {settings.SERVER_HOST}:{settings.SERVER_PORT}")
    server.serve_forever()
except KeyboardInterrupt:
    print("Exiting")
    server.socket.close()
    irc.stop_loop()
finally:
    irc_thread.join()
