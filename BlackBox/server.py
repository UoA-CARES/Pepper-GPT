# -*- coding: utf-8 -*-
import select
import socket
import argparse

"""
BB - Black Box Client
PPCtrl - Pepper Controller Client
"""

HOST = '127.0.0.1'
PORT = 12000
BACKLOG = 5
BUFFSIZE = 2048


class Server:
    def __init__(self, host=HOST, port=PORT):
        # Initial the server
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
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
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--port', action="store", dest="port", type=int, required=True)
        given_args = parser.parse_args()
        PORT = given_args.port
        print(PORT)
    except SystemExit as e:  # if the port number is empty
        print(f'Port number error, use the default port: {PORT}')
    finally:
        Server()
