# -*- coding: utf-8 -*-
from translation import Translation
from speechRecognition import SpeechRecog
from client import Client


def translationTest(q):
    """
    flag=1 Translate the input sentence into English
    flag=0 Translate the input sentence into Chinese
    """
    trans = Translation()
    result = trans.baiduTranslate(q, flag=1)  # Baidu Translate
    print("Original Sentence:" + q)
    print(result)


def srTest():
    sr = SpeechRecog()
    while True:
        sr.speechRecognition()


if __name__ == '__main__':
    # q = raw_input("please input the word you want to translate:")
    # q = "我要吃肥肠和炒饭"
    # translationTest(q)
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
