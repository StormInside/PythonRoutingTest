import socket
from ipaddress import ip_address

class Client:

    def __init__(self,
                ip = "10.0.0.2",
                mac = "AA:AA:AA:AA:11:BB",
                gateway = "10.0.0.1",
                port = 9050
                ):

        # self.set_ip(ip)
        self.ip = ip
        self.mac = mac

        self.gateway = gateway
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)

    # def set_ip(self, ip):
    #     self.ip = ip_address(ip)

    def connect_to_router(self, is_local = True):
        try:
            if is_local:
                self.socket.connect(("localhost", self.port))
            else:
                self.socket.connect((self.gateway, self.port))
        except OSError as ex:
            print(ex)

    def wait_for_res(self):
        while True:
            received_message = self.socket.recv(1024)
            received_message = received_message.decode("utf-8")
            print(received_message)


if __name__ == "__main__":
    client = Client()
    client.connect_to_router()
    client.wait_for_res()