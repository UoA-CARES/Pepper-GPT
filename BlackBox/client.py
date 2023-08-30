# -*- coding: utf-8 -*-
import psutil
import socket
import sys


def get_ip_address(adapter_name):
    addrs = psutil.net_if_addrs()
    if adapter_name in addrs:
        addresses = addrs[adapter_name]
        for addr in addresses:
            if addr.family == socket.AF_INET:
                return addr.address
    return None


# Using Port forwarding to connect the localhost and the virtual machine
# WLAN:8000 (localhost) -> ens33:12000 (VM)
adapter_name = "WLAN"
clientName = "BlackBox"
SERVER_HOST = get_ip_address(adapter_name)  # localhost ip address
SERVER_PORT = 8000  # Port forwarding - without VPN
# SERVER_PORT = 8080  # Port forwarding
BUFF_SIZE = 2048


class Client:
    def __init__(self):
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__client.connect((SERVER_HOST, SERVER_PORT))
            print("Connect to Server successfully!")
            self.dataSend(clientName)

        except Exception as e:
            print(f"The connection to {SERVER_HOST}:{SERVER_PORT} failed.")
            print("Server does not exist!")
            sys.exit()

    def dataSend(self, msg):
        self.__client.sendall(msg.encode())

    def dataRecv(self):
        msg = self.__client.recv(BUFF_SIZE)
        msg = msg.decode()
        return msg

    def close(self):
        self.__client.close()

