# -*- coding: utf-8 -*-
import select
import socket

"""
BB - Black Box Client
PPCtrl - Pepper Controller Client

Msg format:
@ : BB -> PPCtrl, answer from ChatGPT
$ : BB -> PPCtrl, signal for presenting thinking behaviour
"""

HOST = '127.0.0.1'
PORT = 12000
BACKLOG = 5
BUFFSIZE = 2048


class Server:
    def __init__(self):
        # Initial the server
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
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
                    self.clientList[clientName] = client
                else:  # If clients send data to the server
                    data = s.recv(BUFFSIZE)
                    data = data.decode()
                    print(data)
                    if data:
                        if data[0] == '@':  # BB send msg to PPCtrl for speech
                            msg = data[1:]
                            client = self.clientList["PepperCtrl"]
                            client.sendall(msg.encode())
                            
                        if data[0] == '$':  # BB send msg to PPCtrl for action
                            pass

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
