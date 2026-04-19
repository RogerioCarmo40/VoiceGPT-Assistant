import pyaudio
import wave

class AudioHandler:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
        self.format = pyaudio.paInt16
        self.channels = 1
        self.chunk = 1024

    def record(self, duration=5):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format, channels=self.channels,
                        rate=self.sample_rate, input=True,
                        frames_per_buffer=self.chunk)
        print("* Gravando...")
        frames = []
        for _ in range(0, int(self.sample_rate / self.chunk * duration)):
            frames.append(stream.read(self.chunk))
        print("* Gravação finalizada.")
        stream.stop_stream()
        stream.close()
        p.terminate()
        return b''.join(frames)

    def save(self, audio_data, filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(self.format))
        wf.setframerate(self.sample_rate)
        wf.writeframes(audio_data)
        wf.close()