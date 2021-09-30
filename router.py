import socket
from ipaddress import ip_address, ip_network, IPv4Interface
import threading
import json


class Router:

    def __init__(self, hostname, interfaces):

        self.hostname = hostname

        self.interfaces = interfaces
        self.ip_list = [str(self.interfaces[i]["interface"].ip) for i in interfaces]

        self.__create_broadcast()

        self.data_packet = {"src_ip": "ip", "dst_ip": "ip", "data": "message"}
        self.broadcast_packet = {"src_ip": "ip", "data": "message"}

        self.connections = {}
        self.threads = {}

        self.routing_table = {ip_network('192.168.0.0/28')}

    def __create_broadcast(self):
        for interface in self.interfaces:
            broadcast_port = self.interfaces[interface]["br_port"]
            broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            broadcast_socket.bind(('localhost', broadcast_port))
            self.interfaces[interface]["br_socket"] = broadcast_socket

    def _get_ip_lport(self, l_port):
        for interface in self.interfaces:
            if self.interfaces[interface]["l_port"] == l_port:
                return self.interfaces[interface]["interface"].ip

    def connect_to_router(self, ip, l_port):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', l_port))
        sock.listen(1)
        self.connections[l_port] = {"remote_ip": ip, "remote_port": l_port, "connection": sock}
        # print(sock) #
        waiter = threading.Thread(target=self.wait_connection, args=(l_port,))
        waiter.start()
        self.threads[f"{l_port}_waiter"] = waiter

    def wait_connection(self, port):
        connection = self.connections[port]
        sock = connection["connection"]
        conn, addr = sock.accept()
        print(f"Router {self.hostname} CONNECTED to {connection['remote_ip']}")
        self.connections[port]["connection"] = conn
        # print(conn) #
        listener = threading.Thread(target=self.listen_conn, args=(port,))
        listener.start()
        self.threads[f"{port}_listener"] = listener

    def accept_connection(self, r_port, l_port, ip):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect(('localhost', r_port))
        self.connections[l_port] = {"remote_ip": ip, "remote_port": r_port, "connection": connection}
        # print(connection) #
        listener = threading.Thread(target=self.listen_conn, args=(l_port,))
        listener.start()
        self.threads[f"{l_port}_listener"] = listener

    def message_to_connection(self, message, local_port):
        connection = self.connections[local_port]
        conn = connection["connection"]
        packet = self.data_packet
        packet["data"] = message
        packet["src_ip"] = str(self._get_ip_lport(local_port))
        packet["dst_ip"] = str(connection["remote_ip"])
        packet = json.dumps(packet)
        conn.send(bytes(packet, "utf-8"))

    def message_to_broadcast(self, message, interface="All"):
        def send_data(interface):
            sock = self.interfaces[interface]["br_socket"]
            port = self.interfaces[interface]["br_port"]
            packet = self.broadcast_packet
            packet["src_ip"] = str(self.interfaces[interface]["interface"].ip)
            packet["data"] = message
            packet = json.dumps(packet)
            sock.sendto(bytes(packet, "utf-8"), ('<broadcast>', port))

        if interface != "All":
            send_data(interface)
        else:
            for interface in self.interfaces:
                send_data(interface)

    def listen_conn(self, port):
        connection = self.connections[port]["connection"]
        while True:
            message = connection.recv(1024)
            message = message.decode("utf-8")
            if not message:
                break

            print(f"Router {self.hostname} gets '{message}'")

    def listen_broadcast(self):
        def listener(sock):
            while True:
                data, addr = sock.recvfrom(1024)
                data = data.decode("utf-8")
                data = json.loads(data)
                if data["src_ip"] not in self.ip_list:
                    self.parse_broadcast_data(data, addr)

        for interface in self.interfaces:
            broadcast_listener = threading.Thread(target=listener, args=(self.interfaces[interface]["br_socket"], ))
            broadcast_listener.start()
            self.threads[f"broadcast_listener{interface}"] = broadcast_listener

    def parse_broadcast_data(self, data, addr):
        print(f"Router {self.hostname} received '{data}' from broadcast {addr}")

    def start(self):
        self.listen_broadcast()
        print(f"Router {self.hostname} have started")
