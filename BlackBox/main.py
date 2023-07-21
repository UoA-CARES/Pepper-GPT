# -*- coding: utf-8 -*-
from speechRecognition import SpeechRecog
from client import Client
from chatGPT import gptAPI

import threading
from threading import Thread
from threading import Timer

client = Client()
sr = SpeechRecog()
gpt = gptAPI()


def thinking():
    client.dataSend("$Thinking...")
    print("Thinking...")


class GPT_Thread(Thread):

    # A flag to set the state of the thread (pause/runnable)
    __runnable = threading.Event()
    isReplied = False

    def __init__(self):
        super().__init__()
        self.gpt = gpt
        self.reply = ""
        self.pause()

    def run(self):
        while True:
            self.__runnable.wait()
            timer = Timer(2.0, thinking)  # Set the timer for thinking behaviour
            sr.recording()
            timer.start()
            content = sr.speechRecognition()  # Rec the audio for speech recognition
            if content is None:
                self.reply = "@Sorry, I cannot hear you clearly. Please repeat your words."
                timer.cancel()

                print(f"Pepper-GPT: {self.reply}")
                client.dataSend(self.reply)
                print(f"PepperCtrl: {client.dataRecv()}")
            else:
                if content.lower() == "stop":  # Force quit
                    client.close()
                    break

                # Make thinking action before answering or doing physical actions
                self.reply = gpt.askChat(content)
                timer.cancel()
                print(f"Pepper-GPT: {self.reply}")
                client.dataSend(self.reply)
                # Theoretically, there is no need for receiving twice data
                # But maintain following operation can accurately pass the end flag
                # after pepper robot complete its task (Speech)
                # P.s. Actions has not be tested
                client.dataRecv()
                print(f"PepperCtrl: {client.dataRecv()}")

            """msg = input('> ')
            timer = Timer(2.0, thinking)
            timer.start()
            self.reply = self.gpt.askChat(msg)
            timer.cancel()
            client.dataSend(self.reply)
            print(f"Pepper-GPT: {self.reply}")
            print(f"PepperCtrl: {client.dataRecv()}")"""
            # self.pause()

    def getReply(self):
        return self.reply

    def setMsg(self, msg):
        self.msg = msg

    def pause(self):
        self.__runnable.clear()

    def resume(self):
        self.__runnable.set()

    def isFinished(self):
        return self.__runnable.isSet()


if __name__ == '__main__':
    gpt = gptAPI()
    chat = GPT_Thread()
    chat.start()
    chat.resume()

"""if __name__ == '__main__':
    # Initialise the modules
    sr = SpeechRecog()
    gpt = gptAPI()
    client = Client()

    while True:
        content = sr.speechRecognition()  # Rec the audio for speech recognition
        reply = ""
        if content is None:
            reply = "@Sorry, I cannot hear you clearly. Please repeat your words."
            print(reply)
        else:
            client.dataSend(f"SR content = {content}")
            if content.lower() == "stop":  # Force quit
                client.close()
                break

            # Make thinking action before answering or doing physical actions
            # client.dataSend("$Thinking")
            reply = gpt.askChat(content)
            print(f"Pepper-GPT: {reply}")
        client.dataSend(reply)
        client.dataRecv()"""
