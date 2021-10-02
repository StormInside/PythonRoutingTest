from tabulate import tabulate
import threading
import time
from ipaddress import ip_address, ip_network, IPv4Interface

from Router import Router
from Interface import Interface


class Simulation:
    
    def __init__(self):
        self.routers = {}

    def add_router(self, router_name, router_interfaces):
        self.routers[router_name] = Router(router_name, router_interfaces)

    def start_routers(self):
        for router in self.routers:
            self.routers[router].start()


if __name__ == "__main__":
    sim = Simulation()

    # r1_interfaces = {0: {"l_port": 9101, "br_port": 9910, "interface": IPv4Interface('10.1.1.1/24')},
    #                  1: {"l_port": 9102, "br_port": 9920, "interface": IPv4Interface('10.1.2.1/24')},
    #                  2: {"l_port": 9103, "br_port": 9930, "interface": IPv4Interface('10.1.3.1/24')},
    #                  3: {"l_port": 9104, "br_port": 9940, "interface": IPv4Interface('10.1.4.1/24')}}
    #
    # r2_interfaces = {0: {"l_port": 9201, "br_port": 9910, "interface": IPv4Interface('10.2.1.1/24')},
    #                  1: {"l_port": 9202, "br_port": 9920, "interface": IPv4Interface('10.2.2.1/24')},
    #                  2: {"l_port": 9203, "br_port": 9930, "interface": IPv4Interface('10.2.3.1/24')},
    #                  3: {"l_port": 9204, "br_port": 9940, "interface": IPv4Interface('10.2.4.1/24')}}
    #
    # r3_interfaces = {0: {"l_port": 9301, "br_port": 9910, "interface": IPv4Interface('10.3.1.1/24')},
    #                  1: {"l_port": 9302, "br_port": 9920, "interface": IPv4Interface('10.3.2.1/24')},
    #                  2: {"l_port": 9303, "br_port": 9930, "interface": IPv4Interface('10.3.3.1/24')},
    #                  3: {"l_port": 9304, "br_port": 9940, "interface": IPv4Interface('10.3.4.1/24')}}
    r1_interfaces = [Interface(0, 9101, 9910, IPv4Interface('10.1.1.1/24')),
                     Interface(1, 9102, 9920, IPv4Interface('10.1.2.1/24')),
                     Interface(2, 9103, 9930, IPv4Interface('10.1.3.1/24')),
                     Interface(3, 9104, 9940, IPv4Interface('10.1.4.1/24'))]

    r2_interfaces = [Interface(0, 9201, 9910, IPv4Interface('10.2.1.1/24')),
                     Interface(1, 9202, 9920, IPv4Interface('10.2.2.1/24')),
                     Interface(2, 9203, 9930, IPv4Interface('10.2.3.1/24')),
                     Interface(3, 9204, 9940, IPv4Interface('10.2.4.1/24'))]

    r3_interfaces = [Interface(0, 9101, 9910, IPv4Interface('10.3.1.1/24')),
                     Interface(1, 9302, 9920, IPv4Interface('10.3.2.1/24')),
                     Interface(2, 9303, 9930, IPv4Interface('10.3.3.1/24')),
                     Interface(3, 9304, 9940, IPv4Interface('10.3.4.1/24'))]

    sim.add_router("router1", r1_interfaces)
    sim.add_router("router2", r2_interfaces)
    sim.add_router("router3", r3_interfaces)

    time.sleep(1)

    working_routers = {}
    for router in sim.routers:
        sim.routers[router].start()

    time.sleep(1)

    sim.routers["router1"].interfaces[0].connect_to_router("10.0.2.1")
    sim.routers["router2"].interfaces[0].accept_connection(9101, "10.0.1.1")
    sim.routers["router2"].interfaces[1].connect_to_router("10.0.3.1")
    sim.routers["router3"].interfaces[0].accept_connection(9202, "10.0.2.1")
    # #
    sim.routers["router2"].message_to_interface("HELLO", 0)
    time.sleep(1)
    sim.routers["router1"].message_to_interface("REPLY", 0)
    time.sleep(1)
    sim.routers["router2"].message_to_interface("HELLO", 1)
    time.sleep(1)
    sim.routers["router3"].message_to_interface("REPLY", 0)

    # sim.routers["router1"].message_to_broadcast("Hello, can you hear?", 0)
    # sim.routers["router2"].message_to_broadcast("Hello, I can hear", 1)
    # sim.routers["router2"].message_to_broadcast("Hello, I can hear")



