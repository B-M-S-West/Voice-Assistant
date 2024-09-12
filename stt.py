import os
import torch
import torchaudio
from dotenv import load_dotenv
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor

load_dotenv()

MODELS_DIRECTORY = os.getenv("MODELS_DIRECTORY", "models")
MODEL_NAME = os.getenv("AUDIO_MODEL_NAME", "whisper-large-v3")
EXPECTED_SAMPLE_RATE = 16000  # Replace with the expected sample rate for your model

class Audio:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.model = None
            cls._instance.processor = None
        return cls._instance

    def _load_model(self):
        if self.model is None:
            load_dir = os.path.join(MODELS_DIRECTORY, MODEL_NAME)
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = AutoModelForSpeechSeq2Seq.from_pretrained(load_dir).to(self.device)
            self.processor = AutoProcessor.from_pretrained(load_dir)

    def _unload_model(self):
        self.model = None
        self.processor = None

    def transcribe(self, audio):
        self._load_model()
        inputs = self.processor(audio, sampling_rate=EXPECTED_SAMPLE_RATE, return_tensors="pt", language='en').to(self.device)
        with torch.no_grad():
            output = self.model.generate(**inputs)
        transcription = self.processor.batch_decode(output, skip_special_tokens=True)[0]
        self._unload_model()
        return transcription

def speech_to_text(audio_file):
    audio = Audio()
    waveform, sample_rate = torchaudio.load(audio_file)
    waveform_resampled = torchaudio.functional.resample(waveform, orig_freq=sample_rate, new_freq=EXPECTED_SAMPLE_RATE) #change sample rate to 16000 to match training. 
    sample = waveform_resampled.numpy()[0]
    return audio.transcribe(sample)

if __name__ == "__main__":
    question_text = speech_to_text('recorded_audio.wav')
    print(question_text)