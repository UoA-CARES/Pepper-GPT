# coding=utf-8
import naoqi
from naoqi import ALProxy
from actions import Actions
import re


class Pepper:

    def __init__(self, ip='172.22.1.21', port='9559'):
        self.ip = ip
        self.port = port
        print(self.ip, self.port)

        # set the language of pepper robot
        tts = ALProxy("ALTextToSpeech", self.ip, self.port)
        tts.setLanguage("English")

        # set the speech mode of pepper robot
        speak_move_service = ALProxy("ALSpeakingMovement", self.ip, self.port)
        speak_move_service.setMode("contextual")

        # set the listening mode of pepper robot
        listen_move_service = ALProxy("ALListeningMovement", self.ip, self.port)
        listen_move_service.setEnabled(False)
        listen_service = ALProxy("ALSpeechRecognition", self.ip, self.port)
        listen_service.pause(True)
        listen_service.removeAllContext()

        self.agent = Actions(self.ip, self.port)
        print("Pepper Initialise Successfully.")

    def __getCommand(self, msg):
        isAction = False
        prefix = msg[0]
        cmd = msg[1:]
        if prefix == '$':
            isAction = True
        elif prefix == '@':
            isAction = False
        else:
            pass
        return isAction, cmd

    def execute(self, msg):  # execute the command from users
        isAction, cmd = self.__getCommand(msg)
        if isAction:  # execute physical actions
            cmd = cmd.lower()
            self.__action(cmd)
            print("Action", cmd)
        else:  # speech the content
            self.__speech(cmd)
            print("Speech", cmd)

    def __speech(self, content):
        tts = ALProxy("ALAnimatedSpeech", self.ip, self.port)
        speech = ""
        tts.say(content)

    def __action(self, action):
        for key in self.agent.actions_dict.keys():
            if key in action or action in key:
                value = self.agent.actions_dict[key]
                value()
                break
        else:
            self.agent.notExistReply()



"""if __name__ == '__main__':
    c = Client()
    pp = Pepper(ip='172.22.1.21')

    while True:
        msg = "BlackBox: "
        command = c.dataRecv()
        msg += command
        print(msg)
        pp.execute(command)
        if msg == 'BlackBox: -':
            c.close()
            break
        c.dataSend("!")"""
