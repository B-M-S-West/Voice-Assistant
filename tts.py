import os
import nltk
import numpy as np
import torch
import sounddevice as sd
from dotenv import load_dotenv
from transformers import AutoProcessor, BarkModel, pipeline
from IPython.display import Audio
import scipy

load_dotenv()

MODELS_DIRECTORY = os.getenv("MODELS_DIRECTORY", "models")
TTS_MODEL_NAME = os.getenv("TTS_MODEL_NAME", "bark-small")

def text_to_speech(text):
    load_dir = os.path.join(MODELS_DIRECTORY, TTS_MODEL_NAME)

    synthesiser = pipeline("text-to-speech", load_dir)

    speech = synthesiser(text, forward_params={"do_sample": True})

    scipy.io.wavfile.write("bark_out.wav", rate=speech["sampling_rate"], data=speech["audio"])


if __name__ == "__main__":
    text_to_speech(
        '''Hello! I'm Gemma, an AI assistant created by the Gemma team.  
Think of me as a helpful computer program that can understand your questions and requests in plain language, then generate human-like text responses.
What can I help you with today? 😊''')
    