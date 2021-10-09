import socket
from ipaddress import ip_address, ip_network
import threading
import json


class Router:

    def __init__(self, hostname, interfaces):

        self.hostname = hostname

        self.interfaces = interfaces

        self.ip_list = []

        for interface in self.interfaces:
            self.ip_list.append(str(interface.get_ip()))
            interface.hostname = self.hostname
            interface.routing_function = self.__parse_interface_data

        self.__create_broadcast()

        self.data_packet = {"src_ip": "ip", "dst_ip": "ip", "data": "message"}
        self.broadcast_packet = {"src_ip": "ip", "src_port": "port", "data": "message"}

        self.threads = {}

        # self.routing_table = {"network": {"gateway": "0.0.0.0", "interface": 0, "metric": 20}}
        self.routing_table = {}

    def __create_broadcast(self):
        for interface in self.interfaces:
            broadcast_port = interface.broadcast_port
            broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            broadcast_socket.bind(('localhost', broadcast_port))
            interface.broadcast_socket = broadcast_socket

    def __listen_broadcast(self):
        def listener(sock, interface):
            while True:
                data, addr = sock.recvfrom(1024)
                data = data.decode("utf-8")
                data = json.loads(data)
                if data["src_ip"] not in self.ip_list:
                    self.__parse_broadcast_data(data, interface)

        for interface in self.interfaces:
            broadcast_listener = threading.Thread(target=listener, args=(interface.broadcast_socket, interface))
            broadcast_listener.start()
            self.threads[f"broadcast_listener{interface}"] = broadcast_listener

    def __parse_broadcast_data(self, data, interface):
        if data["data"] == "Hello, lets connect":
            if interface.status != "Connected":
                interface.connect_to_router(data["src_ip"])
                self.message_to_broadcast("Ok, Im ready", interface.number)
        if data["data"] == "Ok, Im ready":
            if interface.status != "Connected":
                interface.accept_connection(data["src_port"], data["src_ip"])
        # print(f"Router {self.hostname} received '{data}' from broadcast")

    def __parse_interface_data(self, message):
        print(self.hostname, message)
        message_un = json.loads(message)
        message_ip = ip_address(message_un["dst_ip"])
        if self.has_ip(message_ip):
            print(f"Router {self.hostname} gets '{message_un['data']}' from {message_un['src_ip']}")
        else:
            interface_number = self.__find_route(message_ip)
            if interface_number:
                self.message_to_interface(message_un['data'], interface_number, message_un['src_ip'], message_un["dst_ip"])
            else:
                print(f"Router {self.hostname} dont have route to send data from {message_un['src_ip']}")

    def __find_route(self, ip):
        possible_routes = {}
        for route in self.routing_table:
            if ip_address(ip) in route:
                possible_routes[self.routing_table[route]['metric']] = (self.routing_table[route]['interface'])
        if possible_routes:
            route = possible_routes[min(possible_routes)]
            return route
        return None

    def has_ip(self, message_ip):
        for interface in self.interfaces:
            if interface.get_ip() == message_ip:
                return True
        return False

    def message_to_interface(self, message, interface_number, src_ip=None, dst_ip=None):
        connection = self.interfaces[interface_number].get_conn()
        conn = connection["connection"]
        packet = self.data_packet
        packet["data"] = message
        if src_ip:
            packet["src_ip"] = src_ip
        else:
            packet["src_ip"] = str(self.interfaces[interface_number].get_ip())
        if dst_ip:
            packet["dst_ip"] = dst_ip
        else:
            packet["dst_ip"] = str(connection["remote_ip"])
        packet = json.dumps(packet)
        conn.send(bytes(packet, "utf-8"))

    def message_to_ip(self, message, ip):
        for interface in self.interfaces:
            if ip == interface.connection["remote_ip"]:
                self.message_to_interface(message, interface.number)
                return 0

        interface_number = self.__find_route(ip)
        self.message_to_interface(message, interface_number, str(self.interfaces[interface_number].get_ip()), ip)

    def message_to_broadcast(self, message, interface="All"):
        def send_data(interface):
            sock = interface.broadcast_socket
            port = interface.broadcast_port
            packet = self.broadcast_packet
            packet["src_ip"] = str(interface.get_ip())
            packet["src_port"] = interface.local_port
            packet["data"] = message
            packet = json.dumps(packet)
            sock.sendto(bytes(packet, "utf-8"), ('<broadcast>', port))

        if interface != "All":
            send_data(self.interfaces[interface])
        else:
            for interface in self.interfaces:
                send_data(interface)

    def set_default_route(self, gateway, interface, metric=20):
        network = ip_network('0.0.0.0/0.0.0.0')
        self.routing_table[network] = {"gateway": gateway, "interface": interface, "metric": metric}

    def add_route(self, network, netmask, gateway, interface, metric):
        network = ip_network(f'{network}/{netmask}')
        self.routing_table[network] = {"gateway": gateway,
                                       "interface": interface,
                                       "metric": metric}

    def start(self):
        self.__listen_broadcast()
        print(f"Router {self.hostname} have started")
