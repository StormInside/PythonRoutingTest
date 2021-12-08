from abc import abstractmethod


class RoutingProtocol:

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def add_route(self):
        pass




