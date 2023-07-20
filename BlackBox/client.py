# -*- coding: utf-8 -*-
import socket
import sys
from chatGPT import gptAPI

import threading
from threading import Thread
from threading import Timer

clientName = "BlackBox"
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12000
BUFFSIZE = 2048


class Client:
    def __init__(self, *args):
        if args:
            for arg in args:
                # SERVER_PORT = arg
                print(SERVER_PORT)
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__client.connect((SERVER_HOST, SERVER_PORT))
            print("Connect to Server successfully!")
            self.dataSend(clientName)

        except Exception as e:
            print(SERVER_PORT)
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


"""client = Client()


def thinking():
    client.dataSend("$Thinking...")
    print("Thinking...")


class GPT_Thread(Thread):

    # A flag to set the state of the thread (pause/runnable)
    __runnable = threading.Event()
    isReplied = False

    def __init__(self, gpt):
        super().__init__()
        self.gpt = gpt
        self.reply = ""
        self.pause()

    def run(self):
        while True:
            self.__runnable.wait()
            msg = input('> ')
            timer = Timer(2.0, thinking)
            timer.start()
            self.reply = self.gpt.askChat(msg)
            timer.cancel()
            client.dataSend(self.reply)
            print(f"Pepper-GPT: {self.reply}")
            print(f"PepperCtrl: {client.dataRecv()}")
            # self.pause()

    def getReply(self):
        return self.reply

    def setMsg(self, msg):
        self.msg = msg

    def pause(self):
        self.__runnable.clear()

    def resume(self):
        self.__runnable.set()

    def isFinished(self):
        return self.__runnable.isSet()


if __name__ == '__main__':
    gpt = gptAPI()
    chat = GPT_Thread(gpt)
    chat.start()
    chat.resume()"""

