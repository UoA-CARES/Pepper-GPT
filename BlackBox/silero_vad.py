import torch
from speechRecog import SpeechRecog


class Silero_vad:
    def __init__(self):
        self.SAMPLING_RATE = 16000
        USE_ONNX = False  # change this to True if you want to test onnx model
        self.model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                           model='silero_vad',
                                           force_reload=True,
                                           onnx=USE_ONNX)

        (self.get_speech_timestamps,
         self.save_audio,
         self.read_audio,
         self.VADIterator,
         self.collect_chunks) = utils

    def detect(self, wavefile):
        wav = self.read_audio(wavefile, sampling_rate=self.SAMPLING_RATE)
        speech_timestamp = self.get_speech_timestamps(wav, self.model, sampling_rate=self.SAMPLING_RATE)
        return speech_timestamp


if __name__ == '__main__':
    sr = SpeechRecog()
    vad = Silero_vad()
    while True:
        input(">> press Enter for stop")
        sr.listen()
        sr.sr_openai_whisper('output')
        timestamp = vad.detect('output.wav')
        print(timestamp)
