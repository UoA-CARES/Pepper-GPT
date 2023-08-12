# -*- coding: utf-8 -*-
from client import Client
from speechRecog import SpeechRecog

if __name__ == '__main__':
    client = Client()
    sr = SpeechRecog()
    while True:
        msg = sr.listen()
        print(msg)
        print(type(msg))
        client.dataSend(msg)
        print(client.dataRecv())
