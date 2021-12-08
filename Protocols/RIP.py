import threading
import time

from Protocols.RoutingProtocol import RoutingProtocol


class RIP(RoutingProtocol):

    def __init__(self, router):
        RoutingProtocol.__init__(self, "RIP")
        self.router = router



    def add_route(self):
        pass

    def find_route(self):
        for interface in self.router.interfaces:
            print(self.router.hostname + str(interface.number))
            # self.router.add_route('192.168.0.0', '255.255.0.0', '192.168.0.1', 2, 10)

    def runner(self):
        while True:
            self.find_route()
            time.sleep(5)

    def start(self):
        runner = threading.Thread(target=self.runner, )
        runner.start()

if __name__ == '__main__':
    rip = RIP()
    print(rip.name)
    rip.add_route()
