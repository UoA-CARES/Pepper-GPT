# -*- coding: utf-8 -*-
from threading import Timer

from client import Client
from speechRecog import SpeechRecog
from chatGPT import gptAPI


def thinking():
    client.dataSend("$think")
    print("Thinking...")
    client.dataRecv()


if __name__ == '__main__':
    client = Client()
    sr = SpeechRecog()
    sr.sr_openai_whisper("output")
    gpt = gptAPI()
    gpt._isAction("Hi.")
    temp = input("Press Enter to start.")

    greeting = "@^start(animations/Stand/Gestures/Hey_1)Hello, world! My name is Pepper-GPT.Nice to meet you." \
               " ^wait(animations/Stand/Gestures/Hey_1) "
    client.dataSend(greeting)
    client.dataRecv()

    while True:
        timer = Timer(3, thinking)  # Set the timer for thinking behaviour
        content = sr.listen()
        timer.start()
        content = sr.sr_openai_whisper("output")
        if content is None or content == "":
            reply = "@Sorry, I cannot hear you clearly. Please repeat your words."
            timer.cancel()
        else:
            if content.lower().strip()[:-1] == "stop":  # Force quit
                timer.cancel()
                client.close()
                break

            # Make thinking action before answering or doing physical actions
            reply = gpt.askChat(content)
            timer.cancel()
        print(f"Pepper-GPT: {reply}")
        client.dataSend(reply)
        print(f"PepperCtrl: {client.dataRecv()}")
