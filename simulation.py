from tabulate import tabulate
import threading

from client import Client
from router import Router

class Simulation:
    
    def __init__(self, clients_amount, routers_amount):

        self.routers = {}
        for i in range(1, routers_amount+1):
            self.routers[f"router{i}"] = Router(ip = f"10.0.0.{i}", mac = f"AA:AA:AA:AA:1{i}:AA")

        self.clients = {}
        for i in range(1, clients_amount+1):
            self.clients[f"client{i}"] = Client(ip = f"10.0.0.10{i}", mac = f"AA:AA:AA:AA:1{i}:BB", port=8050+i)


        for router in self.routers:
            for client in self.clients:
                if self.clients[client].gateway == self.routers[router].ip:
                    self.routers[router].add_client(self.clients[client].ip, self.clients[client].mac, self.clients[client].port)

        
    def router_accept(self):
        for router in self.routers:
            self.routers[router].listen_interface()
            self.routers[router].accept_client()

    def client_connect(self):
        for client in self.clients:
                self.clients[client].connect_to_router()

    def print_data(self):
        client_data = {"Name": [], "Ip": [], "Mac": [], "Gateway": [], "Port": []}
        for client in self.clients:
            client_data["Name"].append(client)
            client_data["Ip"].append(self.clients[client].ip)
            client_data["Mac"].append(self.clients[client].mac)
            client_data["Gateway"].append(self.clients[client].gateway)
            client_data["Port"].append(self.clients[client].port)

        router_data = {"Name": [], "Ip": [], "Mac": []}
        for router in self.routers:
            router_data["Name"].append(router)
            router_data["Ip"].append(self.routers[router].ip)
            router_data["Mac"].append(self.routers[router].mac)

        print("Clients")
        print(tabulate(client_data, headers="keys", tablefmt="grid", stralign='center'))
        print("\nRouters")
        print(tabulate(router_data, headers="keys", tablefmt="grid", stralign='center'))


    def start_sim(self):
        pass


if __name__ == "__main__":
    sim = Simulation(5, 1)
    sim.print_data()

    my_thread = threading.Thread(target=sim.router_accept)
    my_thread.start()
    my_thread2 = threading.Thread(target=sim.client_connect)
    my_thread2.start()