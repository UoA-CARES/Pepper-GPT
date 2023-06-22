# -*- coding: utf-8 -*-
import openai

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

    def __init__(self):
        openai.api_key = API_KEY
        self.__msg = [
            {"role": "system", "content": "You are a helpful robot assistant named as Pepper-GPT, a robot incoporate "
                                          "with GPT API."}
        ]

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
        r = Reply()
        if "True" in result:
            r.setAction(True)
            action = result.split(",")[1].strip()[:-1]
            r.setContent(action)
            print(action)
        else:
            r.setAction(False)

        return r

    def __chatHistory(self):  # Generate the chat history after conversation
        pass

    def setMessage(self, role, msg):
        self.__msg.append({"role": role, "content": msg})

    def askChat(self, msg):
        reply = self.__isAction(msg)  # classify the reply type

        if reply.isAction():  # Physical Action
            prompt = f"Please {reply.getContent()}"
            self.setMessage("user", prompt)
            self.setMessage("assistant", "I cannot do physical action but I am embedded in pepper robot so the robot "
                                         "will do it.")
            print(f"Pepper robot will do the action {reply.getContent()}")
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
            print(f"ChatGPT: {reply}")

    """
    def setInputMsg(self, msg):
        self.msg.append({"role": "user", "content": msg})
        self.q = msg

    def askGPT(self):
        chatReply = openai.ChatCompletion.create(
            model=MODEL_ENGINE,
            messages=self.msg,
            max_tokens=512,
            temperature=0.6
        )
        reply = chatReply.choices[0].message.content
        self.msg.append({"role": "assistant", "content": reply})
        print(f"ChatGPT: {reply}")

        q = f"Does the following content ask gpt to do physical actions? Just tell me True or False: {self.q}"
        response = openai.ChatCompletion.create(
            model=MODEL_ENGINE,
            messages=[{"role": "user", "content": q}],
            max_tokens=2,
            temperature=0
        )
        print(f"isPhysicalAction = {response.choices[0].message.content}")

    """


if __name__ == '__main__':
    gpt = gptAPI()
    gpt.askChat("I am so happy today, as a wave of joy washes over me. The sun is shining brightly, and a sense of "
                "contentment fills my heart. Life's beauty surrounds me, and it feels like a perfect moment to "
                "celebrate. With this happiness overflowing, would you mind dancing for me?")
    gpt.askChat("Thanks.")
