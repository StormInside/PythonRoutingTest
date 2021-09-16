import socket
from ipaddress import ip_address

from client import Client


class Router:

    def __init__(
                self,
                ip="10.0.0.1",
                port=9050
                ):
        
        self.ip = ip_address(ip)
        self.port = port
        self.client_interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.client = Client(self.ip+1, self.port)

    def listen_client(self, max_con=1):
        self.client_interface.bind(("", self.port))
        self.client_interface.listen(max_con)

    def accept_client(self):
        client_conn, address = self.client_interface.accept()
        self.client_conn = client_conn
        print(f"Accepted client, address = {address}")

    def message_to_client(self, message):
        self.client_conn.send(bytes(message, "utf-8"))

    def receive_message(self, soc):
        received_message = soc.recv(1024)
        received_message = received_message.decode("utf-8")
        return received_message

    def start(self):
        print(f"Router {self.ip} have started")
        while True:
            message = self.receive_message(self.client_conn)
            if not message:
                break
            print(f"Router {self.ip} gets '{message}' from {self.client.ip}")

    def __del__(self):
        self.client_interface.close()
