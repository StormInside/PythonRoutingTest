import socket
from ipaddress import ip_address
import threading
import json


class Router:

    def __init__(
                self,
                ip="10.0.0.1",
                broadcast_port=9060,
                unused_interfaces=[9101,9102,9103,9104],
                routing_protocol=None
                ):
        
        self.ip = ip_address(ip)
        self.broadcast_port = broadcast_port

        self.broadcast_interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_interface.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcast_interface.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broadcast_interface.bind(('localhost', self.broadcast_port))

        self.unused_interfaces = unused_interfaces

        self.data_packet = {"src_ip": "ip", "dst_ip": "ip", "data": "message"}
        self.broadcast_packet = {"src_ip": str(self.ip), "data": "message"}

        self.connections = {}
        self.threads = {}

        self.routing_protocol = routing_protocol
        self.routing_table = {}

    def connect_to_router(self, ip):
        port = self.unused_interfaces[0]
        if not port:
            return 0
        self.unused_interfaces.pop(0)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', port))
        sock.listen(1)

        self.connections[port] = {"remote_ip": ip, "remote_port": port, "connection": sock}

        waiter = threading.Thread(target=self.wait_connection, args=(port,))
        waiter.start()
        self.threads[f"{port}_waiter"] = waiter

    def wait_connection(self, port):
        connection = self.connections[port]
        sock = connection["connection"]
        conn, addr = sock.accept()
        print(f"Router {self.ip} CONNECTED to {connection['remote_ip']}")
        self.connections[port]["connection"] = conn
        listener = threading.Thread(target=self.listen_conn, args=(port,))
        listener.start()
        self.threads[f"{port}_listener"] = listener

    def accept_connection(self, port, ip):
        connection_port = self.unused_interfaces[0]
        self.unused_interfaces.pop(0)
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect(('localhost', port))
        self.connections[connection_port] = {"remote_ip": ip, "remote_port": port, "connection": connection}
        listener = threading.Thread(target=self.listen_conn, args=(connection_port,))
        listener.start()
        self.threads[f"{connection_port}_listener"] = listener

    def message_to_connection(self, message, local_port):
        connection = self.connections[local_port]
        conn = connection["connection"]
        packet = self.data_packet
        packet["data"] = message
        packet["src_ip"] = str(self.ip)
        packet["dst_ip"] = str(connection["remote_ip"])
        packet = json.dumps(packet)
        conn.send(bytes(packet, "utf-8"))



    def message_to_broadcast(self, message):
        packet = self.broadcast_packet
        packet["data"] = message
        packet = json.dumps(packet)
        self.broadcast_interface.sendto(bytes(packet, "utf-8"), ('<broadcast>', self.broadcast_port))

    def listen_conn(self, port):
        connection = self.connections[port]["connection"]
        while True:
            message = connection.recv(1024)
            message = message.decode("utf-8")
            if not message:
                break

            print(f"Router {self.ip} gets '{message}'")

    def listen_broadcast(self):
        def listener():
            while True:
                data, addr = self.broadcast_interface.recvfrom(1024)
                data = data.decode("utf-8")
                data = json.loads(data)
                if data["src_ip"] != str(self.ip):
                    self.parse_broadcast_data(data, addr)

        broadcast_listener = threading.Thread(target=listener)
        broadcast_listener.start()
        self.threads["broadcast_listener"] = broadcast_listener

    def parse_broadcast_data(self, data, addr):
        print(f"Router {self.ip} received '{data}' from broadcast {addr}")

    def start(self):
        self.listen_broadcast()
        print(f"Router {self.ip} have started")
