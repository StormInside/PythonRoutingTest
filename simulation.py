from tabulate import tabulate
import threading
import time

from client import Client
from router import Router


class Simulation:
    
    def __init__(self):
        self.routers = {}
        self.clients = {}

    def add_client(self, client_name, client_ip, client_mac, gateway):
        self.clients[client_name] = Client(ip=client_ip, mac=client_mac, gateway=gateway)

    def add_router(self, router_name, router_ip, router_mac, port):
        self.routers[router_name] = Router(ip=router_ip, mac=router_mac, port=port)

    def add_clients_to_routers(self):
        for router in self.routers:
            for client in self.clients:
                if self.clients[client].gateway == self.routers[router].ip:
                    self.clients[client].port = self.routers[router].port
                    self.routers[router].add_client(self.clients[client].ip, self.clients[client].mac)

    def router_accept(self):
        for router in self.routers:
            self.routers[router].listen_interfaces()
            self.routers[router].accept_client()

    def client_connect(self):
        for client in self.clients:
            self.clients[client].connect_to_router()

    def start_routers(self):
        for router in self.routers:
            self.routers[router].start()

    def print_data(self):
        client_data = {"Name": [], "Ip": [], "Mac": [], "Gateway": []}
        for client in self.clients:
            client_data["Name"].append(client)
            client_data["Ip"].append(self.clients[client].ip)
            client_data["Mac"].append(self.clients[client].mac)
            client_data["Gateway"].append(self.clients[client].gateway)

        router_data = {"Name": [], "Ip": [], "Mac": [], "Port": []}
        for router in self.routers:
            router_data["Name"].append(router)
            router_data["Ip"].append(self.routers[router].ip)
            router_data["Mac"].append(self.routers[router].mac)
            router_data["Port"].append(self.routers[router].port)

        print("Clients")
        print(tabulate(client_data, headers="keys", tablefmt="grid", stralign='center'))
        print("\nRouters")
        print(tabulate(router_data, headers="keys", tablefmt="grid", stralign='center'))
        print("")


if __name__ == "__main__":
    sim = Simulation()

    clients_amount = 3

    sim.add_router("router1", "10.0.0.1", "AA:AA:AA:AA:11:AA", 9051)
    sim.add_router("router2", "10.0.0.2", "AA:AA:AA:AA:12:AA", 9052)

    for i in range(1, clients_amount+1):
        sim.add_client(f"client{i}", f"10.0.0.10{i}", f"AA:AA:AA:AA:1{i}:BB", "10.0.0.1")

    for i in range(1, clients_amount+1):
        sim.add_client(f"client1{i}", f"10.0.0.20{i}", f"AA:AA:AA:AA:2{i}:BB", "10.0.0.2")

    sim.add_clients_to_routers()

    sim.print_data()

    router_accept = threading.Thread(target=sim.router_accept)
    router_accept.start()
    client_connect = threading.Thread(target=sim.client_connect)
    client_connect.start()

    time.sleep(1)

    working_clients = {}
    for client in sim.clients:
        tread = threading.Thread(target=sim.clients[client].start)
        tread.start()
        working_clients[client] = tread

    print()

    working_routers = {}
    for router in sim.routers:
        tread = threading.Thread(target=sim.routers[router].start)
        tread.start()
        working_routers[router] = tread

    print()

    sim.clients["client3"].send_message("10.0.0.1", "Hello Router")
    sim.clients["client1"].send_message("10.0.0.1", "Hello Router")
    sim.clients["client13"].send_message("10.0.0.1", "Hello Router")
    sim.clients["client2"].send_message("10.0.0.103", "Hello Another Client")


