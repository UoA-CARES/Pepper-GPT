# coding=utf-8
import threading

from client import Client
from pepper import Pepper

IP = '172.22.1.21'
PORT = 9559


if __name__ == '__main__':
    client = Client()
    pp = Pepper(IP, PORT)

    while True:
        content = client.dataRecv()
        if content == '-':  # PPCtrl is required to close the client
            pp.auto.setState("interactive")
            print("PepperController is closing ...")
            client.close()
            break
        else:  # execute the cmds
            try:
                pp.execute(content.encode('utf-8'))  # Convert unicode into string
            except Exception as e:
                print("An error occured: ", e)
                pp.execute("@Sorry I cannot execute it, the reply may has multiple language in it. Please change the "
                           "content.")  # Warning
            client.dataSend("!")  # Send a signal to BlackBox for continue audio rec


