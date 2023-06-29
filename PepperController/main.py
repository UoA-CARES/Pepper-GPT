# coding=utf-8
import naoqi
from naoqi import ALProxy
from client import Client
from pepper import Pepper


IP = '172.22.1.21'
PORT = 9559

if __name__ == '__main__':
    client = Client()
    pp = Pepper(IP, PORT)
    pp.execute("@Hello, world!")

    while True:
        content = client.dataRecv()
        if content == '-':  # PPCtrl is required to close the client
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

