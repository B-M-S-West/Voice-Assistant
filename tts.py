import pyttsx3

def text_to_speech(text):
    # Initialize the TTS engine
    speaker = pyttsx3.init()
    # Set properties (optional)
    speaker.setProperty('rate', 200)  # Speed of speech (words per minute)
    speaker.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
    # Convert text to speech and play it
    speaker.say(text)
    # Wait for the speech to finish
    speaker.runAndWait()

if __name__ == "__main__":
    text_to_speech(
        '''Hello! I'm Gemma, an AI assistant created by the Gemma team.  
Think of me as a helpful computer program that can understand your questions and requests in plain language, then generate human-like text responses.
What can I help you with today? 😊''')
    