from tabulate import tabulate
import threading
import time

from router import Router


class Simulation:
    
    def __init__(self):
        self.routers = {}

    def add_router(self, router_name, router_ip, broadcast_port, unused_interfaces):
        self.routers[router_name] = Router(router_ip, broadcast_port, unused_interfaces)

    def start_routers(self):
        for router in self.routers:
            self.routers[router].start()


if __name__ == "__main__":
    sim = Simulation()

    sim.add_router("router1", "10.0.1.1", 9060, [9101, 9102, 9103, 9104])
    sim.add_router("router2", "10.0.2.1", 9060, [9201, 9202, 9203, 9204])
    sim.add_router("router3", "10.0.3.1", 9060, [9301, 9302, 9303, 9304])

    time.sleep(1)

    working_routers = {}
    for router in sim.routers:
        sim.routers[router].start()

    time.sleep(1)

    sim.routers["router1"].connect_to_router("10.0.2.1")
    sim.routers["router2"].accept_connection(9101, "10.0.1.1")
    sim.routers["router2"].connect_to_router("10.0.3.1")
    sim.routers["router3"].accept_connection(9202, "10.0.2.1")

    sim.routers["router2"].message_to_connection("HELLO", 9201)
    time.sleep(1)
    sim.routers["router1"].message_to_connection("REPLY", 9101)
    time.sleep(1)
    sim.routers["router2"].message_to_connection("HELLO", 9202)
    time.sleep(1)
    sim.routers["router3"].message_to_connection("REPLY", 9301)

    sim.routers["router1"].message_to_broadcast("Hello, can you hear?")
    sim.routers["router2"].message_to_broadcast("Hello, I can hear")



