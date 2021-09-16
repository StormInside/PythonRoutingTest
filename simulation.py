from tabulate import tabulate
import threading
import time

from router import Router


class Simulation:
    
    def __init__(self):
        self.routers = {}

    def add_router(self, router_name, router_ip, port):
        self.routers[router_name] = Router(ip=router_ip, port=port)

    def create_clients(self):
        for router in self.routers:
            self.routers[router].listen_client()

    def connect_clients(self):
        for router in self.routers:
            self.routers[router].client.connect()
            self.routers[router].accept_client()

    def start_routers(self):
        for router in self.routers:
            self.routers[router].start()

    def start_clients(self):
        for router in self.routers:
            self.routers[router].client.start()

    def print_data(self):

        router_data = {"Name": [], "Ip": [], "Port": []}
        for router in self.routers:
            router_data["Name"].append(router)
            router_data["Ip"].append(self.routers[router].ip)
            router_data["Port"].append(self.routers[router].port)

        print("Routers")
        print(tabulate(router_data, headers="keys", tablefmt="grid", stralign='center'))
        print("")


if __name__ == "__main__":
    sim = Simulation()

    sim.add_router("router1", "10.0.1.1", 9051)
    sim.add_router("router2", "10.0.2.1", 9052)

    sim.print_data()

    router_accept = threading.Thread(target=sim.create_clients)
    router_accept.start()
    client_connect = threading.Thread(target=sim.connect_clients)
    client_connect.start()

    time.sleep(1)

    working_clients = {}
    for router in sim.routers:
        tread = threading.Thread(target=sim.routers[router].client.start)
        tread.start()
        working_clients[router] = tread

    print()

    working_routers = {}
    for router in sim.routers:
        tread = threading.Thread(target=sim.routers[router].start)
        tread.start()
        working_routers[router] = tread

    print()

    for router in sim.routers:
        sim.routers[router].client.send_message("Hello Router")

    print()
    time.sleep(1)

    sim.routers["router1"].message_to_client("Hello Client")

    print()
    time.sleep(10)

    for router in sim.routers:
        sim.routers[router].client.send_message("Hello Router")

    print()
    time.sleep(1)

    sim.routers["router1"].message_to_client("World Client")
    sim.routers["router2"].message_to_client("World Client")


