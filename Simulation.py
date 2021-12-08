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

    def __str__(self):
        data = {"Router": [], "Number": [], "Port": [], "Broadcast": [], "IP": [], "Status": []}
        for router in self.routers:
            for interface in self.routers[router].interfaces:
                data["Router"].append(interface.hostname)
                data["Number"].append(interface.number)
                data["Port"].append(interface.local_port)
                data["Broadcast"].append(interface.broadcast_port)
                data["IP"].append(interface.get_ip())
                data["Status"].append(interface.status)

        return tabulate(data, headers='keys', tablefmt='grid')


if __name__ == "__main__":
    sim = Simulation()

    r1_interfaces = [Interface(0, 9101, 9910, IPv4Interface('10.1.1.1/24')),
                     Interface(1, 9102, 9920, IPv4Interface('10.1.2.1/24')),
                     # Interface(2, 9103, 9990, IPv4Interface('10.1.3.1/24')),
                     # Interface(3, 9104, 9990, IPv4Interface('10.1.4.1/24'))
                     ]

    r2_interfaces = [Interface(0, 9201, 9910, IPv4Interface('10.2.1.1/24')),
                     # Interface(1, 9202, 9930, IPv4Interface('10.2.2.1/24')),
                     # Interface(2, 9203, 9990, IPv4Interface('10.2.3.1/24')),
                     # Interface(3, 9204, 9990, IPv4Interface('10.2.4.1/24'))
                     ]

    r3_interfaces = [Interface(0, 9301, 9920, IPv4Interface('10.3.1.1/24')),
                     Interface(1, 9302, 9930, IPv4Interface('10.3.2.1/24')),
                     # Interface(2, 9303, 9990, IPv4Interface('10.3.3.1/24')),
                     # Interface(3, 9304, 9990, IPv4Interface('10.3.4.1/24'))
                     ]

    r4_interfaces = [Interface(0, 9401, 9930, IPv4Interface('10.4.1.1/24')),
                     # Interface(1, 9302, 9930, IPv4Interface('10.3.2.1/24')),
                     # Interface(2, 9303, 9990, IPv4Interface('10.3.3.1/24')),
                     # Interface(3, 9304, 9990, IPv4Interface('10.3.4.1/24'))
                     ]

    sim.add_router("router1", r1_interfaces)
    sim.add_router("router2", r2_interfaces)
    sim.add_router("router3", r3_interfaces)
    sim.add_router("router4", r4_interfaces)

    time.sleep(1)

    working_routers = {}
    for router in sim.routers:
        sim.routers[router].start()

    time.sleep(1)

    sim.routers["router1"].message_to_broadcast("Hello, lets connect")
    time.sleep(1)
    sim.routers["router2"].message_to_broadcast("Hello, lets connect")
    time.sleep(1)
    sim.routers["router3"].message_to_broadcast("Hello, lets connect")
    time.sleep(1)
    print(sim)

    # time.sleep(1)
    sim.routers["router2"].set_default_route("10.1.1.1", 0)
    sim.routers["router3"].set_default_route("10.1.1.1", 0)
    sim.routers["router2"].message_to_ip("HELLO", "10.4.1.1")
    sim.routers["router2"].dynamic_protocol.find_route()
    print(sim.routers["router2"].routing_table)
    # print(sim)





