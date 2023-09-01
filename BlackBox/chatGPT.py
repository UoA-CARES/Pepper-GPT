# -*- coding: utf-8 -*-
import sys

import openai
import logging
from datetime import datetime
import os

API_KEY = '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'
MODEL_ENGINE = "gpt-3.5-turbo"
logger = logging.getLogger('my_logger')


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
        openai.api_key = API_KEY  # Set the key of GPT API
        self.__initLog()  # Initial the logger

        # set the background of conversation
        self.__msg = [
            {"role": "system", "content": "You are a helpful robot assistant named as Pepper-GPT, a robot incorporate "
                                          "with GPT API. All your reply should less than 50 words."
                                          "All your reply should less than 50 words."}
        ]
        logger.info("system: You are a helpful robot assistant named as Pepper-GPT, "
                    "a robot incorporate with GPT API. All your reply should less than 50 words.")

    def __initLog(self):  # Config the logger
        logger.setLevel(logging.INFO)

        # Set the name of log file
        time = datetime.now().strftime("%y%m%d_%H-%M-%S")
        fileName = f"./log/chatHistory_{time}.log"
        print(fileName)
        # Create the file handler
        file_handler = logging.FileHandler(fileName)

        # Config the format of handler
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler into logger
        logger.addHandler(file_handler)

    def _isAction(self, prompt):  # Justify whether the prompt is for physical behaviour
        msg = [
            {"role": "system", "content": "I want you to act as a robot to analyse the input command. "
                                          "Your answer should with the format: "
                                          "'True/False, what physical action (infinitive form).'"
                                          "For example, when you are asked 'Can you dance?', response 'True, dance'"
                                          "For example, when you are asked 'Please show muscle.',"
                                          "response 'True, show muscle'"
                                          "For example, when you are asked 'Do you sing?', response 'True, sing'"},
            {"role": "user", "content": "Please analyse following content, does it ask you to do physical action? "
                                        "What physical action are asked? Answer with the format "
                                        "'True/False, what physical action (infinitive form).'"
                                        f"{prompt}"}]
        response = openai.ChatCompletion.create(
            model=MODEL_ENGINE,
            messages=msg,
            max_tokens=10,
            temperature=0
        )
        result = f"PhysicalAction = {response.choices[0].message.content}"
        print(result)

        if "True" in result:
            self.r.setAction(True)
            action = result.split(",")[1].strip()
            self.r.setContent(action)
        else:
            self.r.setAction(False)

    def setMessage(self, role, msg):
        self.__msg.append({"role": role, "content": msg})
        logger.info(f"{role}: {msg}")

    def askChat(self, msg):
        self._isAction(msg)  # classify the reply type

        if self.r.isAction():  # Physical Action
            prompt = self.r.getContent()
            return self.doActions(prompt)
        else:  # Speech
            msg = f"{msg} (answer in 50 words)"
            self.setMessage("user", msg)
            chatReply = openai.ChatCompletion.create(
                model=MODEL_ENGINE,
                messages=self.__msg,
                max_tokens=150,
                temperature=0.6
            )
            reply = chatReply.choices[0].message.content
            if ("I'm sorry, but" in reply or "As a robot" in reply) and "physical" in reply:  # double check whether GPT analyse correctly
                prompt = self.find_and_get_next_word(reply, "like")[:-3]
                if prompt is None:
                    return self.doActions("NoneAction")
                return self.doActions(prompt)
            self.setMessage("assistant", reply)
            speech = f"@{reply}"
            return speech

    def doActions(self, prompt):
        action = f"Please {prompt}"
        self.setMessage("user", action)
        self.setMessage("assistant",
                        "I cannot do physical action but I am embedded in pepper robot so the robot "
                        "will do it.")
        print(f"Pepper robot will do the action {prompt}")
        action = f"${prompt}"
        return action

    def find_and_get_next_word(self, sentence, target_word):
        index = sentence.find(target_word)

        if index != -1:  # Target word found in the sentence
            # Find the next space character after the target word
            next_space = sentence.find(" ", index)

            if next_space != -1:  # There is a space after the target word
                # Extract the next word after the target word
                next_word_start = next_space + 1
                next_word_end = sentence.find(" ", next_word_start)
                if next_word_end == -1:
                    next_word_end = len(sentence)
                next_word = sentence[next_word_start:next_word_end]
                return next_word
            else:
                return None  # No word found after the target word
        else:
            return None  # Target word not found in the sentence




"""if __name__ == '__main__':
    content = "I'm sorry, but as an AI language model, I don't have a physical body or the ability to perform " \
              "physical actions like rotating my head. I'm here to assist you with information and answer your " \
              "questions to the best of my abilities. "
    target_word = "like"
    next_word = gptAPI().find_and_get_next_word(content, target_word)[:-3]

    if next_word:
        print(f"The word after '{target_word}' is '{next_word}'.")
    else:
        print(f"No word found after '{target_word}'.")"""
