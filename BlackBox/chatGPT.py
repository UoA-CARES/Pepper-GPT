# -*- coding: utf-8 -*-
import openai
import logging
from datetime import datetime

API_KEY = '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'
MODEL_ENGINE = "gpt-3.5-turbo"


class Reply:

    def __init__(self):
        self.__isAction = False
        self.__content = ""

    def setAction(self, b):
        self.__isAction = b

    def setContent(self, msg):
        self.__content = msg

    def isAction(self):
        return self.__isAction

    def getContent(self):
        return self.__content


class gptAPI:

    r = Reply()

    def __init__(self):
        openai.api_key = API_KEY  # set the key of GPT API

        # Config the log record
        time = datetime.now().strftime("%y%m%d_%H-%M-%S")
        fileName = f"chatHistory_{time}.log"
        # fileName = 'chatHist_2023-06-26.log'
        logging.basicConfig(filename=fileName, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # set the background of conversation
        self.__msg = [
            {"role": "system", "content": "You are a helpful robot assistant named as Pepper-GPT, a robot incorporate "
                                          "with GPT API."}
        ]
        logging.info("system: You are a helpful robot assistant named as Pepper-GPT, "
                     "a robot incorporate with GPT API.")

    def __isAction(self, prompt):  # Justify whether the prompt is for physical behaviour
        msg = [{"role": "user", "content": "Please using the format: 'True/False, what physical action (infinitive "
                                           "form).' to answer the question. Does the following input content ask gpt "
                                           "to do physical action? What physical action are asked?"
                                           f"{prompt}"}]
        response = openai.ChatCompletion.create(
            model=MODEL_ENGINE,
            messages=msg,
            max_tokens=10,
            temperature=0
        )
        result = f"PhysicalAction = {response.choices[0].message.content}"

        if "True" in result:
            self.r.setAction(True)
            action = result.split(",")[1].strip()[:-1]
            self.r.setContent(action)
            print(action)
        else:
            self.r.setAction(False)

    def setMessage(self, role, msg):
        self.__msg.append({"role": role, "content": msg})
        logging.info(f"{role}: {msg}")

    def askChat(self, msg):
        self.__isAction(msg)  # classify the reply type

        if self.r.isAction():  # Physical Action
            prompt = f"Please {self.r.getContent()}"
            self.setMessage("user", prompt)
            self.setMessage("assistant", "I cannot do physical action but I am embedded in pepper robot so the robot "
                                         "will do it.")
            print(f"Pepper robot will do the action {self.r.getContent()}")
            pass
        else:  # Speech
            self.setMessage("user", msg)
            chatReply = openai.ChatCompletion.create(
                model=MODEL_ENGINE,
                messages=self.__msg,
                max_tokens=512,
                temperature=0.6
            )
            reply = chatReply.choices[0].message.content
            self.setMessage("assistant", reply)


if __name__ == '__main__':
    gpt = gptAPI()
    gpt.askChat("I am so happy today, as a wave of joy washes over me. The sun is shining brightly, and a sense of "
                "contentment fills my heart. Life's beauty surrounds me, and it feels like a perfect moment to "
                "celebrate. With this happiness overflowing, would you mind dancing for me?")
    gpt.askChat("Thanks.")
    gpt.askChat("what is the result of 32766*1?")
