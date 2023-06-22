# coding=utf-8
import naoqi
from naoqi import ALProxy
from client import Client


IP = 'localhost'
PORT = 33179

if __name__ == '__main__':
    tts = ALProxy("ALTextToSpeech", IP, PORT)
    client = Client()
    tts.setLanguage("English")
    tts.say("Hello, world!")
    """
    while True:
        msg = client.dataRecv()
        if msg == '-':
            client.close()
            break
        else:
            tts.say(msg)
    """
