# coding=utf-8
import threading

from client import Client
from pepper import Pepper
import time

IP = '172.22.1.21'
PORT = 9559


if __name__ == '__main__':
    client = Client()
    pp = Pepper(IP, PORT)
    """pp.execute("@^start(animations/Stand/Gestures/Hey_1)Hello, world! "
               "My name is Pepper-GPT."
               "Nice to meet you. ^wait(animations/Stand/Gestures/Hey_1)")"""

    while True:
        content = client.dataRecv()
        if content == '-':  # PPCtrl is required to close the client
            pp.auto.setState("interactive")
            print("PepperController is closing ...")
            client.close()
            break
        else:  # execute the cmds
            pp.execute(content.encode('utf-8'))  # Convert unicode into string
            client.dataSend("!")  # Send a signal to BlackBox for continue audio rec

    """
    while True:
        content = client.dataRecv()
        if content == '-':
            client.close()
            break
        else:
            content = content.encode('utf-8')[1:]  # Convert unicode into string
            tts.say(content)
            client.dataSend("!")  # Send a signal to BlackBox for continue audio rec
    """

