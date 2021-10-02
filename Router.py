import socket
from ipaddress import ip_address, ip_network, IPv4Interface
import threading
import json


class Router:

    def __init__(self, hostname, interfaces):

        self.hostname = hostname

        self.interfaces = interfaces

        self.ip_list = []

        for interface in self.interfaces:
            self.ip_list.append(interface.get_ip())
            interface.hostname = self.hostname

        self.__create_broadcast()

        self.data_packet = {"src_ip": "ip", "dst_ip": "ip", "data": "message"}
        self.broadcast_packet = {"src_ip": "ip", "data": "message"}

        self.threads = {}

        self.routing_table = {}

    def __create_broadcast(self):
        for interface in self.interfaces:
            broadcast_port = interface.broadcast_port
            broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            broadcast_socket.bind(('localhost', broadcast_port))
            interface.broadcast_socket = broadcast_socket

    def message_to_interface(self, message, interface_number):
        connection = self.interfaces[interface_number].get_conn()
        conn = connection["connection"]
        packet = self.data_packet
        packet["data"] = message
        packet["src_ip"] = self.interfaces[interface_number].get_ip()
        packet["dst_ip"] = str(connection["remote_ip"])
        packet = json.dumps(packet)
        conn.send(bytes(packet, "utf-8"))

    def message_to_broadcast(self, message, interface="All"):
        def send_data(interface):
            sock = interface.broadcast_socket
            port = interface.broadcast_port
            packet = self.broadcast_packet
            packet["src_ip"] = interface.get_ip()
            packet["data"] = message
            packet = json.dumps(packet)
            sock.sendto(bytes(packet, "utf-8"), ('<broadcast>', port))

        if interface != "All":
            send_data(self.interfaces[interface])
        else:
            for interface in self.interfaces:
                send_data(interface)

    def listen_broadcast(self):
        def listener(sock):
            while True:
                data, addr = sock.recvfrom(1024)
                data = data.decode("utf-8")
                data = json.loads(data)
                if data["src_ip"] not in self.ip_list:
                    self.parse_broadcast_data(data, addr)

        for interface in self.interfaces:
            broadcast_listener = threading.Thread(target=listener, args=(interface.broadcast_socket, ))
            broadcast_listener.start()
            self.threads[f"broadcast_listener{interface}"] = broadcast_listener

    def parse_broadcast_data(self, data, addr):
        print(f"Router {self.hostname} received '{data}' from broadcast {addr}")

    def start(self):
        self.listen_broadcast()
        print(f"Router {self.hostname} have started")
