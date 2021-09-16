import socket
# from ipaddress import ip_address
import json


class Client:

    def __init__(
                self,
                ip="10.0.0.2",
                mac="AA:AA:AA:AA:11:BB",
                gateway="10.0.0.1",
                port=9050
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

    def connect_to_router(self, is_local=True):
        try:
            if is_local:
                self.socket.connect(("localhost", self.port))
            else:
                self.socket.connect((self.gateway, self.port))
        except OSError as ex:
            print(ex)

    def send_message(self, ip, message):
        packet = json.dumps({"src_ip": self.ip, "dst_ip": ip, "data": message})
        self.socket.send(bytes(packet, "utf-8"))

    def receive_message(self):
        received_message = self.socket.recv(1024)
        received_message = received_message.decode("utf-8")
        received_message = json.loads(received_message)
        return received_message

    def start(self):
        print(f"{self.ip} have started")
        while True:
            try:
                message = self.receive_message()
                print(f"to {self.ip} message '{message['data']}' from {message['src_ip']}")
            except OSError as ex:
                pass


if __name__ == "__main__":
    client = Client()
    client.connect_to_router()

