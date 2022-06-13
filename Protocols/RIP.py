import threading
import time
import copy

from Protocols.RoutingProtocol import RoutingProtocol


class RIP(RoutingProtocol):

    def __init__(self, router):
        RoutingProtocol.__init__(self, "RIP")
        self.router = router
        self.rip_packet = {'type': 'RIP', 'routing_table': None}

    def new_message(self, message, interface):
        routing_table = message['routing_table']
        for network in routing_table:
            metric = routing_table[network]["metric"]
            if network not in self.router.routing_table:
                self.router.routing_table[network] = {
                                        "gateway": interface.get_ip_str(),
                                        "interface": interface.number,
                                        "metric": metric}
                print(f"Update Routing Table {self.router.hostname} "
                      f"From RIP\n   {self.router.routing_table}")
            elif metric < self.router.routing_table[network]["metric"]:
                self.router.routing_table[network] = {
                                        "gateway": interface.get_ip_str(),
                                        "interface": interface.number,
                                        "metric": metric}
                print(f"Update Routing Table {self.router.hostname} "
                      f"From RIP\n   {self.router.routing_table}")

    def get_routing_table_to_send(self):
        r_table = copy.deepcopy(self.router.routing_table)
        for network in r_table:
            r_table[network]['metric'] += 1
        return r_table

    def send_route(self):
        for interface in self.router.interfaces:
            packet = self.rip_packet
            packet['routing_table'] = self.get_routing_table_to_send()
            if packet['routing_table']:
                self.router.message_to_interface(packet, interface.number)

    def runner(self):
        while True:
            time.sleep(5)
            self.send_route()

    def start(self):
        runner = threading.Thread(target=self.runner, )
        runner.start()


if __name__ == '__main__':
    rip = RIP()
    print(rip.name)
