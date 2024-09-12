import tkinter as tk
from tkinter import ttk
from audio_recorder import AudioRecorder
from stt import speech_to_text
from question_answerer import answer_question
from tts import text_to_speech

class VoiceQAApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Voice QA App')
        self.geometry('300x200')
        self.audio_recorder = AudioRecorder()
        self.setup_ui()

    def setup_ui(self):
        self.status_label = ttk.Label(self, text='Click the button to start recording')
        self.status_label.pack(pady=20)

        self.record_button = ttk.Button(self, text='Record Question', command=self.handle_record)
        self.record_button.pack()

    def handle_record(self):
        if self.record_button['text'] == 'Record Question':
            self.record_button['text'] = 'Stop Recording'
            self.status_label['text'] = 'Recording...'
            self.audio_recorder.start_recording()
        else:
            self.record_button['text'] = 'Record Question'
            self.status_label['text'] = 'Processing...'
            self.audio_recorder.stop_recording()
            self.process_audio()

    def process_audio(self):
        audio_file = 'recorded_audio.wav'
        
        # Convert speech to text
        self.status_label['text'] = 'Transcribing audio...'
        question_text = speech_to_text(audio_file)
        self.status_label['text'] = f'Question: {question_text}'

        # Get answer from Ollama model
        self.status_label['text'] = 'Generating answer...'
        answer_text = answer_question(question_text)
        self.status_label['text'] = f'Answer: {answer_text}'

        # Convert answer to speech and play it
        self.status_label['text'] = 'Playing answer...'
        text_to_speech(answer_text)
        self.status_label['text'] = 'Answer played.'

def main():
    app = VoiceQAApp()
    app.mainloop()

if __name__ == "__main__":
    main()