# -*- coding: utf-8 -*-
import sys

import openai
import logging
from datetime import datetime
import os

API_KEY = ''
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
                                        "'True/False, what physical action (infinitive form).'\n\n"
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
        msg = f"{msg} (answer in 50 words)"
        self.setMessage("user", msg)
        chatReply = openai.ChatCompletion.create(
            model=MODEL_ENGINE,
            messages=self.__msg,
            max_tokens=150,
            temperature=0.6
        )
        reply = chatReply.choices[0].message.content
        double_check, action = self.reply_check(reply)  # double check whether GPT analyse correctly

        if self.r.isAction() and double_check:  # Physical Action
            prompt = self.r.getContent()
            return self.doActions(prompt)
        elif not self.r.isAction() and double_check:
            return self.doActions(action)
        else:  # Speech
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

    def reply_check(self, reply):
        if "physical" in reply.lower():
            msg = [
                {"role": "system", "content": "Analyse the user's content and reply in the format '"
                                              "'what physical action (infinitive form)'"},
                {"role": "user", "content": "Please analyse following content, what physical action you cannot do? "
                                            "Please analyse following content, what physical action you cannot do? "
                                            "Answer with the format "
                                            "what physical action (infinitive form):'\n\n"
                                            f"{reply}"}]
            response = openai.ChatCompletion.create(
                model=MODEL_ENGINE,
                messages=msg,
                max_tokens=10,
                temperature=0
            )
            result = f"Double_Check_Result = {response.choices[0].message.content}"
            print(result)

            return True, response.choices[0].message.content

        return False, " "

    def clearHistory(self):
        self.__msg = [
            {"role": "system", "content": "You are a helpful robot assistant named as Pepper-GPT, a robot incorporate "
                                          "with GPT API. All your reply should less than 50 words."
                                          "All your reply should less than 50 words."}
        ]
