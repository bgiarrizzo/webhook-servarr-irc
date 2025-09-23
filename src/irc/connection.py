import select
import time
import sys
import socket
import threading

PING_INTERVAL = 30
PING_TIMEOUT = PING_INTERVAL + 30  # Must be PING_INTERVAL + actual ping timeout
RETRY_INTERVAL = 60

ansi_colors = {
    "green": "1;32m",
    "blue": "1;34m",
    "red": "1;31m",
    "brown": "0;33m",
}


def colorize(line: str, color: str):
    if not sys.stdout.isatty():
        return line
    return "\033[" + ansi_colors[color] + line + "\033[0m"


class IrcConnection:
    def __init__(self, server, channel, nick, passw, port):
        self.server = server
        self.channel = channel
        self.nick = nick
        self.passw = passw
        self.port = port

        self.connection = None
        self.buffer = ""
        self.last_pong = 0
        self.await_pong = False

        self.queue = []
        self.lock = threading.Lock()
        self.quit_loop = False

    def connect_server(self):
        print(colorize(f"Connecting to {self.server}:{self.port}", "brown"))

        while not self.connection:
            try:
                self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection.connect((self.server, self.port))
            except socket.gaierror:
                print(
                    colorize(
                        "Couldn't resolve server, check your internet connection. Re-attempting in 60 seconds.",
                        "red",
                    )
                )
                self.connection = None
                time.sleep(RETRY_INTERVAL)

        self.last_pong = time.time()
        self.await_pong = False

        if self.passw:
            self.post_string(f"PASS {self.passw}\n")

        self.post_string(f"NICK {self.nick}\n")
        self.post_string(f"USER {self.nick} 0 * :{self.nick}\n")
        self.post_string(f"JOIN {self.channel}\n")
        self.send_message(colorize("IRC bot initialized successfully", "green"))

    def reconnect(self):
        assert self.connection is not None

        self.connection.shutdown(2)
        self.connection.close()
        self.connection = None
        self.connect_server()

    def try_ping(self):
        self.post_string(f"PING {self.server}\n")
        self.await_pong = True

    def schedule_message(self, message: str):
        with self.lock:
            self.queue.append(message)

    def process_line(self, line: str):
        if "PING" in line:
            self.post_string(f"PONG {line.split()[1]}\n")
        elif "PONG" in line:
            self.last_pong = time.time()
            self.await_pong = False
        else:
            print(f"{colorize(self.server, 'green')}: {line}")

    def process_input(self):
        assert self.connection is not None

        data = self.connection.recv(4096)
        if not data:
            return

        self.buffer += data.decode("utf-8")
        last_line_complete = self.buffer[-1] == "\n"
        lines = self.buffer.split("\n")
        if last_line_complete:
            lines.append("")

        for line in lines[:-1]:
            self.process_line(line)

        self.buffer = lines[-1]

    def post_string(self, message: str):
        assert self.connection is not None

        print(colorize(self.nick + "> " + message.strip(), "blue"))
        self.connection.send(message.encode("utf-8"))

    def send_message(self, message: str):
        self.post_string(f"NOTICE {self.channel} :{message}\n")

    def stop_loop(self):
        self.quit_loop = True

    def loop(self):
        self.connect_server()
        while not self.quit_loop:
            try:
                to_read, _, _ = select.select([self.connection], [], [], 1)
            except select.error:
                self.reconnect()
                continue

            if self.last_pong + PING_INTERVAL < time.time() and not self.await_pong:
                self.try_ping()

            if self.last_pong + PING_TIMEOUT < time.time() and self.await_pong:
                self.reconnect()
                continue

            if to_read:
                self.process_input()

            with self.lock:
                while self.queue:
                    self.send_message(self.queue.pop(0))

    def __del__(self):
        if self.connection:
            self.connection.close()
