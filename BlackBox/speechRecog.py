# -*- coding: utf-8 -*-
import sys
import wave
import pyaudio
import numpy as np
import whisper


class SpeechRecog:
    def __init__(self):
        self.model = whisper.load_model("small")
        print("Whisper model load successfully.")

    def listen(self):
        try:
            self.record_audio()
        except Exception as e:
            print(f"WARNING!!! : {e}")
            sys.exit()

    def record_audio(self, sample_rate=16000, chunk_size=1024):
        # Initialise the recording settings
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True,
                            frames_per_buffer=chunk_size)
        wav_path = "output.wav"
        seconds = 2
        temp = 20
        min_db = 2000  # Minimal decibel
        delay_time = 1.3
        frames = []
        start = False  # Start recording start
        record = True  # start to determine whether the recording should continue
        stop = False  # start to indicate whether the audio volume is too low to stop the recording

        temp_time = 0
        temp_new_time = 0

        while record:
            data = stream.read(chunk_size, exception_on_overflow=False)
            frames.append(data)
            audio_data = np.frombuffer(data, dtype=np.short)
            temp = np.max(audio_data)

            if temp > min_db and start is False:
                start = True
                print("Start Recording...")
                temp_new_time = temp_time

            if start:
                if temp < min_db and stop is False:
                    stop = True
                    temp_new_time = temp_time

                if temp > min_db:
                    stop = False
                    temp_new_time = temp_time

                if temp_time > temp_new_time + delay_time * 15 and stop is True:
                    print("continue speaking or keep quiet to stop")
                    if stop and temp < min_db:
                        record = False
                    else:
                        stop = False

            temp_time += 1

        print("Finished recording.\n")
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save the recorded audio as a WAV file
        with wave.open(wav_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))

        wf.close()

    def sr_openai_whisper(self, file_name):
        file_path = f"{file_name}.wav"
        try:
            results = self.model.transcribe(file_path, language='en')
            content = ", ".join([i["text"] for i in results["segments"] if i is not None])
            print(f"Recog Result: {content}\n")
            return content
        except Exception as e:
            print(f"WARNING!!! : {e}")
            sys.exit()


if __name__=='__main__':
    s = SpeechRecog()
    s.listen()
    s.sr_openai_whisper("output")
