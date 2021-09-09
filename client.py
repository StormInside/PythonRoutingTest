import socket
import time 
from ipaddress import ip_address

class Client:

    def __init__(self, ip = "10.0.0.2",
                        mac = "AA:AA:AA:AA:11:BB",
                        gateway = ip_address("10.0.0.1"),
                        port = 9050
                        ):
        self.set_ip(ip)
        self.mac = mac

        self.gateway = gateway
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def set_ip(self, ip):
        self.ip = ip_address(ip)

        


# time.sleep(1)
# client1.connect(router)

# while True:
#     received_message = client1.recv(1024)
#     received_message = received_message.decode("utf-8")
    
#     source_mac = received_message[0:17]
#     destination_mac = received_message[17:34]
#     source_ip = received_message[34:45]
#     destination_ip =  received_message[45:56]
#     message = received_message[56:]

#     print("\nPacket integrity:\ndestination MAC address matches client 1 MAC address: {mac}".format(mac=(client1_mac == destination_mac)))
#     print("\ndestination IP address matches client 1 IP address: {mac}".format(mac=(client1_ip == destination_ip)))
#     print("\nThe packed received:\n Source MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
 
#     print("\nSource IP address: {source_ip}, Destination IP address: {destination_ip}".format(source_ip=source_ip, destination_ip=destination_ip))
 
#     print("\nMessage: " + message)

if __name__ == "__main__":
    client = Client(ip = "10.20")