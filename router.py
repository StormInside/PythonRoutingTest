import socket
import json
import threading


class Router:

    def __init__(
                self,
                ip="10.0.0.1",
                mac="AA:AA:AA:AA:11:AA",
                port=9050
                ):
        
        self.ip = ip
        self.mac = mac

        self.port = port

        self.interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.clients = {}
        self.listeners = []

    def add_client(self, client_ip, client_mac):
        self.clients[client_mac] = {"ip": client_ip, "socket": None}

    def listen_interfaces(self, max_con=10, is_local=True):
        self.interface.bind(("", self.port))
        self.interface.listen(max_con)

    def accept_client(self):
        for mac in self.clients:
            client, address = self.interface.accept()
            self.clients[mac]["socket"] = client
            print(f"Accepted client, address = {address}")

    def send_message(self, mac, src_ip, message):
        packet = json.dumps({"src_ip": src_ip, "data": message})
        self.clients[mac]["socket"].send(bytes(packet, "utf-8"))

    def wait_message(self, mac):
        while True:
            message = self.receive_message(self.clients[mac]["socket"])
            if message:
                # print(f"to {self.ip} message '{message['data']}' from {message['src_ip']}")
                self.parse_message(message)

    def parse_message(self, message):
        if message["dst_ip"] != self.ip:
            self.find_path(message)
        else:
            print(f"to {self.ip} message '{message['data']}' from {message['src_ip']}")

    def find_path(self, message):
        arp = {}
        for mac in self.clients:
            arp[self.clients[mac]["ip"]] = mac
        if message["dst_ip"] in arp:
            self.send_message(arp[message["dst_ip"]], message["src_ip"], message["data"])

    def receive_message(self, soc):
        received_message = soc.recv(1024)
        received_message = received_message.decode("utf-8")
        received_message = json.loads(received_message)
        return received_message

    def start(self):
        print(f"{self.ip} have started")
        for mac in self.clients:
            thread = threading.Thread(target=self.wait_message, args=(mac,))
            thread.start()
            self.listeners.append(thread)

    def __del__(self):
        self.interface.close()


if __name__ == "__main__":
    router = Router()
    router.add_client("10.0.0.2", "AA:AA:AA:AA:11:BB", 9050)
