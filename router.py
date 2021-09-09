import socket
import time


class Router:

    def __init__(self,
                ip = "10.0.0.1",
                mac = "AA:AA:AA:AA:11:AA",
                ):
        
        self.ip = ip
        self.mac = mac
        
        self.clients = {}
        self.interfaces = {}

    def add_client(self, client_ip, client_mac, client_port, is_local = True):
        self.clients[client_mac] = [client_ip, client_port]
        self.add_interface(client_port, client_ip, is_local)

    def add_interface(self, client_port, client_ip, is_local = True):
        interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if is_local:
            interface.bind(("localhost", client_port))
        else:
            interface.bind((client_ip, client_port))
        self.interfaces[client_port] = interface

    def listen_interface(self, interface_port = "all"):
        if interface_port == "all":
            for interface in self.interfaces:
                self.interfaces[interface].listen(1)
        else:
            self.interfaces[interface_port].listen(1)

    def accept_client(self):
        for mac in self.clients:
            client, address = self.interfaces[self.clients[mac][1]].accept()
            print(f"client = {client}, address = {address}")


if __name__ == "__main__":
    router = Router()
    router.add_client("10.0.0.2", "AA:AA:AA:AA:11:BB", 9050)