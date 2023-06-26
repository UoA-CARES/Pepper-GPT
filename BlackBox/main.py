# -*- coding: utf-8 -*-
from speechRecognition import SpeechRecog
from client import Client
from chatGPT import gptAPI


if __name__ == '__main__':
    # Initialise the modules
    sr = SpeechRecog()
    gpt = gptAPI()
    client = Client()

    """while True:
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
            reply = gpt.askChat(content)
            print(f"Pepper-GPT: {reply}")
        client.dataSend(reply)
        client.dataRecv()"""
