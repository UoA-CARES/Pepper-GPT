# -*- coding: utf-8 -*-
import socket
import sys
from chatGPT import gptAPI

clientName = "BlackBox"
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12000
BUFFSIZE = 2048


class Client:
    def __init__(self):
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__client.connect((SERVER_HOST, SERVER_PORT))
            print("Connect to Server successfully!")
            self.dataSend(clientName)

        except Exception as e:
            print("Server does not exist!")
            sys.exit()

    def dataSend(self, msg):
        self.__client.sendall(msg.encode())

    def dataRecv(self):
        msg = self.__client.recv(BUFFSIZE)
        msg = msg.decode()
        return msg

    def close(self):
        self.__client.close()


if __name__ == '__main__':
    c = Client()
    # gpt = gptAPI()

    while True:
        msg = input('> ')
        # reply = gpt.askChat(msg)
        # c.dataSend(reply)
        # print(f"Pepper-GPT: {reply}")
        c.dataSend(msg)
        print(f"PepperCtrl: {c.dataRecv()}")

