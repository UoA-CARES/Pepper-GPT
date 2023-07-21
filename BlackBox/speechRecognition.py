import speech_recognition as sr
import pyaudio
import logging
from time import sleep


class SpeechRecog:

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.r = sr.Recognizer()
        p = pyaudio.PyAudio()
        # Microphone
        self.mic = sr.Microphone()
        self.audio = None
        print("If you see messages above, it's not [Black Box]'s fault.")
        print("End of PyAudio initialization.")

    def recording(self):
        sleep(0.8)
        logging.info("Start Recording...")
        with self.mic as source:
            self.r.adjust_for_ambient_noise(source)
            self.audio = self.r.listen(source)
        logging.info("Stop Recording. Analyzing the audio...")

    def speechRecognition(self):
        """sleep(1)
        logging.info("Start Recording...")
        with self.mic as source:
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)
        logging.info("Stop Recording. Analyzing the audio...")"""
        try:
            content = self.r.recognize_google(self.audio, language='zh-CN', show_all=False)
            logging.info("End of Speech Recognition.")
            # print(content)
            # self.client.dataSend(content)
            return content
        except sr.UnknownValueError:
            # raise 'Google Speech Recognition could not understand audio'
            print('Google Speech Recognition could not understand audio')
            return
        except sr.RequestError as e:
            # raise 'Could not request results from Google Speech Recognition Service'
            print('Could not request results from Google Speech Recognition Service')
            return
