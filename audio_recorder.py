import pyaudio
import wave

class AudioRecorder:
    def __init__(self, filename='recorded_audio.wav'):
        self.filename = filename
        self.frames = []
        self.is_recording = False
        self.p = pyaudio.PyAudio()
        self.stream = None

    def start_recording(self):
        self.frames = []
        self.is_recording = True

        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=44100,
                                  input=True,
                                  frames_per_buffer=1024,
                                  stream_callback=self.callback)

        self.stream.start_stream()

    def callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)

    def stop_recording(self):
        self.is_recording = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        self.p.terminate()

        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        print(f"Recording saved as {self.filename}")