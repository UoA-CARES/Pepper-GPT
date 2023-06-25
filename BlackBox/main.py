# -*- coding: utf-8 -*-
from translation import Translation
from speechRecognition import SpeechRecog
from client import Client


if __name__ == '__main__':
    sr = SpeechRecog()
    trans = Translation()
    client = Client()

    while True:
        content = sr.speechRecognition()
        if content is not None:
            client.dataSend(f"SR content = {content}")
            print(f"SR content = {content}")
            # content = input("> ")
            if content == "stop" or ("停" in content):
                client.close()
                break
            result = '@'
            result += trans.baiduTranslate(content, flag=1)
            client.dataSend(result)
        else:
            print("No content has been listened. Please repeat your words.")
