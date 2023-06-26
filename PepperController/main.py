# coding=utf-8
import naoqi
from naoqi import ALProxy
from client import Client


IP = '172.22.1.21'
PORT = 9559

if __name__ == '__main__':
    client = Client()
    tts = ALProxy("ALTextToSpeech", IP, PORT)
    tts.setLanguage("English")
    tts.say("Hello, world!")

    while True:
        content = client.dataRecv()
        if content == '-':
            client.close()
            break
        else:
            content = content.encode('utf-8')  # Convert unicode into string
            tts.say(content)
            print("The speech finish.")
            client.dataSend("!")  # Send a signal to BlackBox for continue audio rec


    """
    while True:
        msg = client.dataRecv()
        if msg == '-':
            client.close()
            break
        else:
            tts.say(msg)
    """
