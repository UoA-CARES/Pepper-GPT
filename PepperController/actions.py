# coding=utf-8
import time
import naoqi
from naoqi import ALProxy
import random

class Actions:

    def __init__(self, ip, port):
        self.tts = ALProxy("ALAnimatedSpeech", ip, port)

        self.action_think = None
        self.content_think = None
        self.action_fitness = None
        self.content_fitness = None
        self.action_content_init()

        self.actions_dict = {}
        self.actions_init()

    def action_content_init(self):
        self.action_think = ["animations/Stand/Gestures/Thinking_1",
                             "animations/Stand/Gestures/Thinking_3",
                             "animations/Stand/Gestures/Thinking_4",
                             "animations/Stand/Gestures/Thinking_6",
                             "animations/Stand/Gestures/Thinking_8"]

        self.content_think = ["Hmmm",
                              "Well",
                              "Just give me a minute to think through this.",
                              "I'm trying to figure it out.",
                              "Hmm, let me see.",
                              "I'm in the process of analyzing.",
                              "Give me a second, I'm thinking.",
                              "Let me think about it."]

        self.action_fitness = ["animations/Stand/Waiting/ShowMuscles_1",
                               "animations/Stand/Waiting/ShowMuscles_2",
                               "animations/Stand/Waiting/ShowMuscles_3",
                               "animations/Stand/Waiting/ShowMuscles_4",
                               "animations/Stand/Waiting/ShowMuscles_5",
                               "animations/Stand/Waiting/Fitness_1"]

        self.content_fitness = ["Look at my muscles!",
                                "I am a strong robot.",
                                "I am supercalifragilisticexpialidocious.",
                                "I've got some serious strength and muscles to show for it!"]

    def think(self):
        action = self.action_think[random.randint(0, len(self.action_think)-1)]
        content = self.content_think[random.randint(0, len(self.content_think)-1)]
        command = "^start(%s) %s...^wait(%s)" % (action, content, action)
        self.tts.say(command)

    def dance(self):
        command = "^start(User/date_dance-fc1190) Please watch. ^wait(User/date_dance-fc1190)"
        self.tts.say(command)
        self.tts.say("Thanks for watching.")
        time.sleep(0.5)

    def guitar(self):
        command = ("^start(animations/Stand/Waiting/AirGuitar_1) Enjoy the music. "
                   "^wait(animations/Stand/Waiting/AirGuitar_1)")
        self.tts.say(command)
        time.sleep(0.5)

    def fitness(self):
        action = self.action_fitness[random.randint(0, len(self.action_fitness) - 1)]
        content = self.content_fitness[random.randint(0, len(self.content_fitness) - 1)]
        command = "^start(%s) %s...^wait(%s)" % (action, content, action)
        print(command)
        self.tts.say(command)

    def sing(self):
        command = (" I can sing Happy Birthday ^start(animations/Stand/Waiting/HappyBirthday_1) song. "
                   "^wait(animations/Stand/Waiting/HappyBirthday_1)")
        self.tts.say(command)
        time.sleep(0.5)

    def rotate(self):
        command = ("I will be in high ^start(animations/Stand/Waiting/Robot_1) speed! "
                   "^wait(animations/Stand/Waiting/Robot_1)")
        self.tts.say(command)

    def actions_init(self):
        self.actions_dict["think"] = self.think
        self.actions_dict["dance"] = self.dance
        self.actions_dict["guitar"] = self.guitar
        self.actions_dict["show"] = self.fitness
        self.actions_dict["sing"] = self.sing
        self.actions_dict["rotate"] = self.rotate

    def notExistReply(self):
        action = self.action_think[random.randint(0, len(self.action_think) - 1)]
        content = "I am sorry but my developer did not design me to do this action."
        command = "^start(%s) %s...^wait(%s)" % (action, content, action)
        self.tts.say(command)


if __name__ == "__main__":
    a = Actions("172.22.1.21", 9559)
    action = a.actions_dict["sing"]
    action()
