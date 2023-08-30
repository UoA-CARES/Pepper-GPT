# -*- coding: utf-8 -*-
import socket
import psutil
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
adapter_name = "ens33"  # without VPN
# adapter_name = "vpn"
clientName = "PepperCtrl"
SERVER_HOST = get_ip_address(adapter_name)  # localhost ip address
SERVER_PORT = 12000  # Port forwarding
BUFF_SIZE = 2048


class Client:
    def __init__(self):
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__client.connect((SERVER_HOST, SERVER_PORT))
            print("Connect to Server successfully!")
            self.__client.sendall(clientName.encode())
        except Exception as e:
            print("The connection to ", SERVER_HOST, ":", SERVER_PORT, " failed.")
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


if __name__ == '__main__':
    c = Client()

    while True:
        msg = "BlackBox: "
        msg += c.dataRecv()
        print(msg)
        if msg == 'BlackBox: -':
            c.close()
            break
        c.dataSend("!")
