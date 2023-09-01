#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use run Method"""
import qi
import naoqi
from naoqi import ALProxy


import qi

def on_animated_speech_end(value):
    print("EndOfAnimatedSpeech event received.")
    # Your code to handle the end of animated speech

if __name__ == "__main__":
    try:

        # Subscribe to the "EndOfAnimatedSpeech" event
        # event_name = "ALAnimatedSpeech/EndOfAnimatedSpeech"
        # memory_service.subscriber(event_name)

        # Start the animated speech
        speak_move_service = ALProxy("ALSpeakingMovement", '172.22.1.21', 9559)
        speak_move_service.setMode("contextual")

        # tts = ALProxy("ALAnimationPlayer", '172.22.1.21', 9559)
        tts = ALProxy("ALBehaviorManager", "172.22.1.21", 9559)
        #temp = tts.startBehavior("91_dance/bahavior")
        temp = tts.getBehaviorNames()
        tts.startBehavior("User/date_dance-fc1190")

        """tts = ALProxy("ALBehaviorManager", self.ip, self.port)
        tts.startBehavior("User/date_dance-fc1190")"""
        # tts.say("^Hello Sophia, nice to meet you. My name is Pepper-GPT, "
        #       "your AI assistant. What can I do for you today?")
        # tts.say("^start(negative)Yes, Jasmine green tea is a popular type of tea from China. It is made by scenting green tea leaves with jasmine flowers, resulting in a fragrant and aromatic brew.Yes, Jasmine green tea is a popular type of tea from China. It is made by scenting green tea leaves with jasmine flowers, resulting in a fragrant and aromatic brew.^wait(negative)")
        # tts.wait()
        # tts.run("91_dance")
        # tts.run("animations/Stand/Gestures/Hey_1")

        # Wait for the event to be triggered (you can perform other tasks here)
        # app.run()

        # Unsubscribe from the event before stopping the application
        # memory_service.unsubscribeToEvent(event_name, "on_animated_speech_end")
    except KeyboardInterrupt:
        print("Interrupted by user.")



