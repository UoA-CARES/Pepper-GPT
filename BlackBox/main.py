# -*- coding: utf-8 -*-
import re
from threading import Timer

from client import Client
from speechRecog import SpeechRecog
from chatGPT import gptAPI


def thinking():
    print("Thinking...")
    client.dataSend("$think")
    client.dataRecv()


def contains_non_english_characters(sentence):
    pattern = r'[^A-Za-z0-9\s\.,;?!-:^_@]+'
    match = re.search(pattern, sentence)
    if match:
        return True
    else:
        return False


if __name__ == '__main__':
    client = Client()
    sr = SpeechRecog()
    sr.sr_openai_whisper("output")
    gpt = gptAPI()
    gpt._isAction("Hi.")  # test gpt connection
    temp = input("Press Enter to start.")

    greeting = "@^start(animations/Stand/Gestures/Hey_1)Hello, world! My name is Pepper-GPT.Nice to meet you." \
               " ^wait(animations/Stand/Gestures/Hey_1) "
    client.dataSend(greeting)
    client.dataRecv()

    while True:
        timer = Timer(2.5, thinking)  # Set the timer for thinking behaviour
        content = sr.listen()
        timer.start()
        content = sr.sr_openai_whisper("output")
        if content is None or content == "":
            reply = "@Sorry, I cannot hear you clearly. Please repeat your words."
            timer.cancel()
        else:
            if content.lower().strip()[:-1] == "stop":  # Force quit
                timer.cancel()
                client.dataRecv()
                client.close()
                break

            # Make thinking action before answering or doing physical actions
            reply = gpt.askChat(content)
            timer.cancel()
        print(f"Pepper-GPT: {reply}")
        if contains_non_english_characters(reply):
            reply = "@Sorry I cannot execute it, the reply may has multiple language in it. Please change the content."
        client.dataSend(reply)
        recv_msg = client.dataRecv()
        print(f"PepperCtrl: {recv_msg}")
