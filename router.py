import socket
from ipaddress import ip_address
import threading

from client import Client


class Router:

    def __init__(
                self,
                ip="10.0.0.1",
                client_port=9050,
                broadcast_port=9060
                ):
        
        self.ip = ip_address(ip)
        self.client_port = client_port
        self.broadcast_port = broadcast_port

        self.client_interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_interface.bind(('localhost', self.client_port))
        
        self.client = Client(self.ip+1, self.client_port)

        self.broadcast_interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_interface.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcast_interface.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broadcast_interface.bind(('localhost', self.broadcast_port))

        self.connections = {}

        self.threads = {}

    def wait_client(self, max_con=1):
        self.client_interface.listen(max_con)

    def accept_client(self):
        client_conn, address = self.client_interface.accept()
        self.client_conn = client_conn
        print(f"Accepted client, address = {address}")

    def message_to_client(self, message):
        self.client_conn.send(bytes(message, "utf-8"))

    def message_to_broadcast(self, message):
        self.broadcast_interface.sendto(bytes(message, "utf-8"), ('<broadcast>', self.broadcast_port))

    def listen_client(self):
        def listener():
            while True:
                message = self.client_conn.recv(1024)
                message = message.decode("utf-8")
                if not message:
                    break

                print(f"Router {self.ip} gets '{message}' from {self.client.ip}")

        client_listener = threading.Thread(target=listener)
        client_listener.start()
        self.threads["client_listener"] = client_listener

    def listen_broadcast(self):
        def listener():
            while True:
                data, addr = self.broadcast_interface.recvfrom(1024)
                data = data.decode("utf-8")
                self.parse_broadcast_data(data, addr)

        broadcast_listener = threading.Thread(target=listener)
        broadcast_listener.start()
        self.threads["broadcast_listener"] = broadcast_listener

    def parse_broadcast_data(self, data, addr):
        print(f"Router {self.ip} received '{data}' from broadcast {addr}")

    def start(self):
        self.listen_client()
        self.listen_broadcast()
        print(f"Router {self.ip} have started")

    def __del__(self):
        self.client_interface.close()
