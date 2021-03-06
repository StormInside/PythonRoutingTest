from Simulation import Simulation
from Interface import Interface
from ipaddress import IPv4Interface
import time


sim = Simulation()

r1_interfaces = [Interface(0, 9101, 9910, IPv4Interface('10.1.1.1/24')),
                 Interface(1, 9102, 9920, IPv4Interface('10.1.2.1/24')),
                 ]

r2_interfaces = [Interface(0, 9201, 9910, IPv4Interface('10.2.1.1/24')),
                 ]

r3_interfaces = [Interface(0, 9301, 9920, IPv4Interface('10.3.1.1/24')),
                 Interface(1, 9302, 9930, IPv4Interface('10.3.2.1/24')),
                 ]

r4_interfaces = [Interface(0, 9401, 9930, IPv4Interface('10.4.1.1/24')),
                 ]

sim.add_router("router1", r1_interfaces)
sim.add_router("router2", r2_interfaces)
sim.add_router("router3", r3_interfaces)
sim.add_router("router4", r4_interfaces)
sim.start_routers()

sim.routers["router1"].message_to_broadcast("Hello, lets connect")
time.sleep(1)
sim.routers["router2"].message_to_broadcast("Hello, lets connect")
time.sleep(1)
sim.routers["router3"].message_to_broadcast("Hello, lets connect")
print(sim)

print(f"Routing table of Router1 is {sim.routers['router1'].routing_table}")

time.sleep(1)
sim.routers["router2"].set_default_route("10.1.1.1", 0)
sim.routers["router3"].set_default_route("10.1.1.1", 0)
sim.routers["router3"].add_route("10.4.1.0", '255.255.255.0', '10.3.2.1', 1, 10)

time.sleep(15)

sim.routers["router2"].message_to_ip("HELLO!", '10.4.1.1')

print()
print(f"Routing table of Router1 is {sim.routers['router1'].routing_table}")
print(f"Routing table of Router2 is {sim.routers['router2'].routing_table}")
print(f"Routing table of Router3 is {sim.routers['router3'].routing_table}")
print()
