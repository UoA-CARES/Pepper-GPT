# coding=utf-8
import naoqi
from naoqi import ALProxy
from client import Client


class Pepper:

    def __init__(self, ip='127.0.0.1', port='9559'):
        self.ip = ip
        self.port = port
        print(self.ip, self.port)

        # set the language of pepper robot
        tts = ALProxy("ALTextToSpeech", self.ip, self.port)
        tts.setLanguage("English")

        # set the speech mode of pepper robot
        speak_move_service = ALProxy("ALSpeakingMovement", '172.22.1.21', 9559)
        speak_move_service.setMode("contextual")

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
            self.__action(cmd)
            print("Action", cmd)
        else:  # speech the content
            self.__speech(cmd)
            print("Speech", cmd)

    def __speech(self, content):
        tts = ALProxy("ALAnimatedSpeech", self.ip, self.port)
        tts.say(content)

    def __action(self, action):
        # tts = ALProxy("ALTextToSpeech", self.ip, self.port)
        # tts.setLanguage("English")
        # tts.say(action)
        tts = ALProxy("ALAnimatedSpeech", self.ip, self.port)
        tts.say("^start(animations/Stand/Gestures/Thinking_8)Well...^wait(animations/Stand/Gestures/Thinking_8)")
        pass


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
