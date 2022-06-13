from abc import abstractmethod


class RoutingProtocol:

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def new_message(self, message, interface):
        pass

