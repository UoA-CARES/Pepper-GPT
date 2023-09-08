# -*- coding: utf-8 -*-
import re
from threading import Timer

from client import Client
from speechRecog import SpeechRecog
from silero_vad import Silero_vad
from chatGPT import gptAPI


def thinking():
    print("Thinking...")
    client.dataSend("$think")
    client.dataRecv()


def contains_non_english_characters(sentence):
    pattern = r'[^A-Za-z0-9\s\.,;?!-:^_@=]+'
    match = re.search(pattern, sentence)
    if match:
        return True
    else:
        return False


if __name__ == '__main__':
    # Initialisation
    client = Client()
    sr = SpeechRecog()
    sv = Silero_vad()
    gpt = gptAPI()

    # API test
    sr.sr_openai_whisper("output")
    sv.detect("output.wav")
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
        if not sv.detect("output.wav"):
            print("No human voice detect, restart recording.")
            timer.cancel()
            continue
        content = sr.sr_openai_whisper("output")
        if content is None or content == "":
            reply = "@Sorry, I cannot hear you clearly. Please repeat your words."
            timer.cancel()
        else:
            if content.lower().strip()[:-1] == "stop":  # Force quit
                timer.cancel()
                print(">> Press e to exit the program")
                print(">> Press s to clear the chat history and start a new conversation")
                print(">> Press c to continue chatting")
                command = input(">> ")
                if command == 'e':
                    client.close()
                    break
                elif command == 's':
                    gpt.clearHistory()
                    input("Press Enter to start.")
                    continue
                elif command == 'c':
                    input("Press Enter to continue.")
                    continue

            # Make thinking action before answering or doing physical actions
            reply = gpt.askChat(content)
            timer.cancel()
        print(f"Pepper-GPT: {reply}")
        if contains_non_english_characters(reply):
            reply = "@Sorry I cannot execute it, the reply may has multiple language in it. Please change the content."
        client.dataSend(reply)
        recv_msg = client.dataRecv()
        print(f"PepperCtrl: {recv_msg}")
