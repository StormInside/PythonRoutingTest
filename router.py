import socket


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

    def add_client(self, client_ip, client_mac):
        self.clients[client_mac] = {"ip": client_ip, "socket": None}
        # self.clients[client_mac]["ip"] = client_ip

    def listen_interfaces(self, max_con=10, is_local=True):
        self.interface.bind(("", self.port))
        self.interface.listen(max_con)

    def accept_client(self):
        for mac in self.clients:
            client, address = self.interface.accept()
            self.clients[mac]["socket"] = client
            print(f"Accepted client, address = {address}")

    def send_message(self, mac, message):
        self.clients[mac]["socket"].send(bytes(message, "utf-8"))

    def receive_message(self, soc):
        received_message = soc.recv(1024)
        received_message = received_message.decode("utf-8")
        return received_message

    def start(self):
        print(f"{self.ip} have started")
        while True:
            for mac in self.clients:
                message = self.receive_message(self.clients[mac]["socket"])
                if not message:
                    break
                print(f"'{message}' from {mac}")

    def __del__(self):
        self.interface.close()


if __name__ == "__main__":
    router = Router()
    router.add_client("10.0.0.2", "AA:AA:AA:AA:11:BB", 9050)
