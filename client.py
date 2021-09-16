import socket


class Client:

    def __init__(self, ip, port):

        self.ip = ip
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)

    def connect(self):
        self.socket.connect(("localhost", self.port))

    def send_message(self, message):
        self.socket.send(bytes(message, "utf-8"))

    def receive_message(self):
        received_message = self.socket.recv(1024)
        received_message = received_message.decode("utf-8")
        return received_message

    def start(self):
        print(f"Client {self.ip} have started")
        while True:
            try:
                message = self.receive_message()
                print(f"Client {self.ip} received '{message}'")
            except OSError as ex:
                pass
