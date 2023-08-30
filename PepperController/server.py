# -*- coding: utf-8 -*-
import select
import socket
import psutil
import sys

"""
BB - Black Box Client
PPCtrl - Pepper Controller Client
"""


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
HOST = get_ip_address(adapter_name)  # localhost ip address
PORT = 12000
BACKLOG = 5
BUFFSIZE = 2048


class Server:
    def __init__(self, host=HOST, port=PORT):
        # Initial the server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(BACKLOG)
        print("Server started listening ", HOST, ": ", PORT)

        # Initial the client connection list
        self.clientList = {}
        self.clientSize = 0
        self.outputs = []

        self.runServer()

    def runServer(self):
        print("Start running the server")
        self.inputs = [self.server]  # list of sockets
        isEnd = False
        while True:
            try:
                readable, writeable, exceptional = select.select(self.inputs, self.outputs, [])
            except select.error as e:
                print(e)
                break

            for s in readable:
                if s == self.server:  # If detect connection from new client
                    print("Waiting to receive msg from client ...")
                    client, addr = self.server.accept()
                    self.inputs.append(client)
                    data = client.recv(BUFFSIZE)
                    if data:
                        print(f"Connect to {addr}: {data.decode()}")
                    else:
                        print("No data received")
                    clientName = data.decode()
                    self.clientList[clientName] = client  # Store the clientList
                else:  # If clients send data to the server
                    data = s.recv(BUFFSIZE)
                    data = data.decode()
                    print(data)
                    if data:
                        if data == '!':  # PPCtrl send msg to BB for next rec
                            client = self.clientList["BlackBox"]
                            client.sendall(data.encode())
                            print("Send to BlackBox 4 next rec")

                        else:  # BB send msg to PPCtrl
                            client = self.clientList["PepperCtrl"]
                            client.sendall(data.encode())

                    else:
                        print("Close the Server ...")
                        client = self.clientList["PepperCtrl"]
                        msg = '-'
                        client.sendall(msg.encode())
                        self.server.close()
                        # self.closeConn()
                        return


if __name__ == '__main__':
    Server()
