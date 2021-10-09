import socket
import threading


class Interface:

    def __init__(self, number, local_port, broadcast_port, interface):
        self.number = number
        self.local_port = local_port
        self.broadcast_port = broadcast_port
        self.interface = interface
        self.status = "Unused"

        self.hostname = None
        self.routing_function = None
        self.broadcast_socket = None
        self.listener = None

        self.connection = {}

    def get_ip(self):
        return self.interface.ip

    def get_conn(self):
        return self.connection

    def connect_to_router(self, r_ip):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', self.local_port))
        sock.listen(1)
        self.connection = {"remote_ip": r_ip, "connection": sock}
        waiter = threading.Thread(target=self.wait_connection)
        waiter.start()
        self.listener = waiter

    def wait_connection(self):
        connection = self.connection
        sock = connection["connection"]
        conn, address = sock.accept()
        print(f"Router {self.hostname} CONNECTED to {connection['remote_ip']}")
        self.connection["connection"] = conn
        # print(conn) #
        self.status = "Connected"
        listener = threading.Thread(target=self.listen_conn)
        listener.start()
        self.listener = listener

    def accept_connection(self, r_port, ip):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect(('localhost', r_port))
        self.connection = {"remote_ip": ip, "remote_port": r_port, "connection": connection}
        # print(connection) #
        self.status = "Connected"
        listener = threading.Thread(target=self.listen_conn)
        listener.start()
        self.listener = listener

    def listen_conn(self):
        connection = self.connection["connection"]
        while True:
            message = connection.recv(1024)
            message = message.decode("utf-8")
            if not message:
                break

            self.routing_function(message)


