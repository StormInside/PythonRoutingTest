from tabulate import tabulate

from Router import Router


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
